from __future__ import annotations

from typing import Any, Callable, Coroutine, Dict, Optional

from fastapi import Request
from jwt import exceptions as jwt_errors
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from application.schemas.user import UserSchema
from config.auth import AuthConfig
from data_access.repository.cache_repository import CacheRepository
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.jwt_auth import decode


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
            raise BaseError(
                error_code=ErrorCodes.MISSING_AUTHORIZATION_HEADER_ERROR,
                message="Authorization header is missing."
            )
        try:
            scheme, token = authorization_header.split()
        except ValueError:
            raise BaseError(
                error_code=ErrorCodes.INVALID_AUTHORIZATION_HEADER_ERROR,
                message="Authorization header format is incorrect."
            )
        if scheme.lower() != 'bearer':
            raise BaseError(
                error_code=ErrorCodes.INVALID_AUTHORIZATION_SCHEME_ERROR,
                message="Invalid authorization scheme. Please use 'Bearer' scheme."
            )
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
        except BaseError as e:
            raise e
        except Exception as e:
            raise BaseError(
                error_code=ErrorCodes.UNKNOWN_ERROR,
                message="An unexpected error occurred. Please try again later."
            )

        return await call_next(request)

    async def _authenticate(self, token: str) -> UserSchema:
        try:
            payload = decode(token, self.config.secret, algorithms=[self.config.algorithm])
            if not payload:
                raise BaseError(
                    error_code=ErrorCodes.INVALID_TOKEN_ERROR,
                    message="The provided token is invalid"
                )

            try:
                request_token_user = UserSchema.model_validate(payload)
            except Exception as e:
                raise BaseError(
                    error_code=ErrorCodes.INTERNAL_AUTHENTICATION_ERROR,
                    message="There was an error validating your session."
                )

            cached_user = await self._fetch_user(token)
            if not cached_user:
                raise BaseError(
                    error_code=ErrorCodes.TOKEN_NOT_FOUND_ERROR,
                    message="Session not found."
                )

            try:
                user = UserSchema.model_validate(cached_user)
            except Exception as e:
                raise BaseError(
                    error_code=ErrorCodes.INTERNAL_AUTHENTICATION_ERROR,
                    message="There was an error validating your session."
                )

            if user.user_id != request_token_user.user_id:
                raise BaseError(
                    error_code=ErrorCodes.IDENTITY_MISMATCH_ERROR,
                    message="User identity mismatch."
                )

            return user
        except jwt_errors.InvalidTokenError as e:
            raise BaseError(
                error_code=ErrorCodes.INVALID_TOKEN_ERROR,
                message="The provided token is invalid."
            )
        except Exception as e:
            raise e

    async def _fetch_user(self, token: str) -> Optional[Dict[str, Any]]:
        cache_key = token
        user_data = await self.cache.get(cache_key)
        if user_data is None:
            raise BaseError(
                error_code=ErrorCodes.CACHE_KEY_NOT_FOUND_ERROR,
                message="Session not found."
            )
        return user_data
