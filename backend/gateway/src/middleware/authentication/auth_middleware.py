from __future__ import annotations

from datetime import timedelta
from typing import Any, Callable, Coroutine, Dict, Optional

from fastapi import Request
from jwt import exceptions as jwt_errors
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from config.auth import AuthConfig
from data_access.repository.cache_repository import CacheRepository
from ftgo_utils.jwt_auth import decode
from application.schemas.user import UserSchema
from middleware.authentication.exceptions import *

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.config = AuthConfig()
        self.cache = CacheRepository.get_cache(self.config.cache_key_prefix)
        self.no_auth_urls = [
            "/auth/register",
            "/auth/verify",
            "/auth/login",
            "/auth/resend_code",
            "/docs",
            "/openapi.json",
        ]

    @classmethod
    def extract_token_from_headers(cls, headers: Headers) -> str:
        authorization_header = headers.get('Authorization')
        if not authorization_header:
            raise MissingAuthorizationHeader()
        try:
            scheme, token = authorization_header.split()
        except ValueError:
            raise UserAuthenticationError('Could not separate Authorization scheme and token')
        if scheme.lower() != 'bearer':
            raise InvalidAuthorizationScheme(scheme)
        return token

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> Response:
        request_url_path = request.url.path
        if any(url in request_url_path for url in self.no_auth_urls):
            return await call_next(request)

        try:
            token = self.extract_token_from_headers(request.headers)
            user = await self._authenticate(token)
            request.state.user = UserSchema.model_validate(user.dict(exclude={'token'}))
        except UserAuthenticationError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

        return await call_next(request)

    async def _authenticate(self, token: str) -> UserSchema:
        try:
            payload = decode(token, self.config.secret, algorithms=[self.config.algorithm])
            if not payload:
                raise TokenDecodingError()

            try:
                request_token_user = UserSchema.model_validate(payload)
            except Exception as e:
                raise UserValidationError(e)

            cached_user = await self._fetch_user(token)
            if not cached_user:
                raise TokenNotFound()

            try:
                user = UserSchema.model_validate(cached_user)
            except Exception as e:
                raise UserValidationError(e)

            if user.user_id != request_token_user.user_id:
                raise IdentityMismatch()

            return user
        except jwt_errors.InvalidTokenError as e:
            raise InvalidToken(f"JWT error: {str(e)}")
        except UserAuthenticationError:
            raise
        except Exception as e:
            raise InternalAuthenticationError(f"Authentication error: {str(e)}")

    async def _fetch_user(self, token: str) -> Optional[Dict[str, Any]]:
        cache_key = token
        return await self.cache.get(cache_key)
