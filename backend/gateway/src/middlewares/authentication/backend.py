from datetime import timedelta
from typing import Optional, Tuple, Dict, Any

from fastapi import FastAPI, Request
from fastapi.security.utils import get_authorization_scheme_param
from jwt import exceptions as jwt_errors
from starlette.authentication import (
    AuthenticationBackend, AuthCredentials, AuthenticationError, BaseUser
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from ftgo_utils.jwt_auth import encode, decode

from config.auth import AuthConfig
from data_access.repository.cache_repository import CacheRepository
from middlewares.authentication.user import FastAPIUser
from schemas.user import UserSchema

class JWTAuthenticationBackend(AuthenticationBackend):
    def __init__(self, cache: CacheRepository, config: AuthConfig, cache_key_prefix="session_token:"):
        self.config = config
        self.cache = cache
        self.cache_key_prefix = cache_key_prefix
        self.cache.set_group(cache_key_prefix)

    @staticmethod
    def middleware_class():
        return AuthenticationMiddleware
    
    @staticmethod
    def middleware_kwargs(auth_config: Optional[AuthConfig] = None, cache_repository: Optional[CacheRepository] = None):
        if cache_repository is None:
            cache_repository = CacheRepository()
        
        if auth_config is None:
            auth_config = AuthConfig.load()
        
        auth_backend = JWTAuthenticationBackend(cache=cache_repository, config=auth_config)
        return dict(
            backend=auth_backend,
        )

    async def authenticate(self, conn: HTTPConnection) -> Optional[Tuple[AuthCredentials, BaseUser]]:
        if any(conn.url.path.startswith(url) for url in self.config.excluded_urls):
            return None
        if "Authorization" not in conn.headers:
            return None
        auth_header = conn.headers["Authorization"]
        scheme, token = get_authorization_scheme_param(auth_header)
        if scheme.lower() != "bearer":
            return None
        return await self._authenticate_token(token)

    async def _authenticate_token(self, token: str) -> Optional[Tuple[AuthCredentials, BaseUser]]:
        try:
            payload = decode(token, self.config.secret, algorithms=[self.config.algorithm])
            user_id = payload.get("sub")
            if not user_id:
                return None

            cached_user = await self.fetch_token(user_id)
            if not cached_user:
                return None

            user_schema = UserSchema(**cached_user)
            user = FastAPIUser(user_schema)
            return AuthCredentials(["authenticated"]), user

        except jwt_errors.InvalidTokenError:
            return None
        except Exception as e:
            raise AuthenticationError(f"Authentication error: {str(e)}")

    async def generate_token(self, user: UserSchema) -> str:
        payload = {"sub": user.user_id, "role": user.role}
        access_token_expires = timedelta(minutes=self.config.access_token_expire_minutes)
        token = encode(
            payload=payload,
            secret=self.config.secret,
            algorithm=self.config.algorithm,
            expiration=access_token_expires.total_seconds()
        )
        await self.cache_token(user.user_id, user.dict(), access_token_expires.total_seconds())
        return token

    async def cache_token(self, user_id: str, user_data: Dict[str, Any], ttl: float):
        cache_key = f"{self.cache_key_prefix}{user_id}"
        await self.cache.set(cache_key, user_data, ttl=ttl)

    async def invalidate_token(self, token: str):
        try:
            payload = decode(token, self.config.secret, algorithms=[self.config.algorithm])
            user_id = payload.get("sub")
            if user_id:
                await self.cache.delete(f"{self.cache_key_prefix}{user_id}")
            else:
                raise AuthenticationError("Invalid token")
        except jwt_errors.InvalidTokenError:
            raise AuthenticationError("Invalid token")

    async def fetch_token(self, user_id: str) -> Optional[Dict[str, Any]]:
        cache_key = f"{self.cache_key_prefix}{user_id}"
        return await self.cache.get(cache_key)
