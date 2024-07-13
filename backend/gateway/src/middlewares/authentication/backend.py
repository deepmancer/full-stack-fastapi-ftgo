from typing import Optional, Tuple, Dict, Type

from fastapi import FastAPI, Request
from starlette.authentication import AuthenticationBackend, AuthCredentials, AuthenticationError, BaseUser
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security.utils import get_authorization_scheme_param

from data_access.repository.cache_repository import CacheRepository
from utils.jwt_token import JWTTokenHandler
from schemas.auth.user import UserSchema
from config.auth import AuthConfig

class JWTAuthenticationBackend(AuthenticationBackend):
    def __init__(self, cache: CacheRepository, config: AuthConfig, cache_key_prefix="session_token:"):
        self.config = config
        self.cache = cache
        self.cache_key_prefix = cache_key_prefix

        self.cache.set_group(cache_key_prefix)

    async def authenticate(self, conn: Type[HTTPConnection]) -> Optional[Tuple[AuthCredentials, BaseUser]]:
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
            payload = JWTTokenHandler.decode(token, self.config.secret, algorithms=[self.config.algorithm])
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
        payload = {"sub": user.user_id, "role": user.role, "scope": user.scope}
        access_token_expires = timedelta(minutes=self.config.access_token_expire_minutes)
        token = JWTTokenHandler.encode(
            payload=payload,
            secret=self.config.secret,
            algorithm=self.config.algorithm,
            expiration=access_token_expires.total_seconds()
        )
        await self.cache_token(user.user_id, user.dict(), access_token_expires.total_seconds())
        return token

    async def cache_token(self, user_id: str, user_data: Dict[str, Any], ttl: float):
        cache_key = user_id
        await self.cache.set(cache_key, user_data, ttl=ttl)

    async def invalidate_token(self, token: str):
        payload = JWTTokenHandler.decode(token, self.config.secret, algorithms=[self.config.algorithm])
        user_id = payload.get("sub")
        if user_id:
            await self.cache.delete(user_id)
        else:
            raise AuthenticationError("Invalid token")

    async def fetch_token(self, user_id: str) -> Optional[Dict[str, Any]]:
        cache_key = user_id
        return await self.cache.get(cache_key)
