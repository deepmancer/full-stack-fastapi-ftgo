import time
from typing import Callable, Coroutine, Any

import jwt.exceptions as jwt_errors
from application.schemas.user import UserStateSchema
from config.auth import AuthConfig
from data_access.repository.cache_repository import CacheRepository
from domain.token_manager import TokenManager
from fastapi import Request
from fastapi.responses import JSONResponse
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.jwt_auth import decode
from middleware import get_logger
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


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
            request.state.user = UserStateSchema.model_validate(user.dict())
        except BaseError as e:
            return self._handle_authentication_exception(request, e)
        except Exception as e:
            error = BaseError(
                error_code=ErrorCodes.INTERNAL_AUTHENTICATION_ERROR,
                message="An unexpected error occurred while processing the authentication token."
            )
            return self._handle_authentication_exception(request, error)

        return await call_next(request)

    async def _authenticate(self, token: str) -> UserStateSchema:
        try:
            payload = decode(token, self.config.secret, algorithms=[self.config.algorithm])
            if not payload:
                raise BaseError(
                    error_code=ErrorCodes.INVALID_TOKEN_ERROR,
                    message="The provided token is not correct."
                )

            try:
                request_token_user = UserStateSchema.model_validate(payload)
            except Exception as e:
                raise BaseError(
                    error_code=ErrorCodes.INTERNAL_AUTHENTICATION_ERROR,
                    message="There was an error validating your session."
                )    
            try:
                user = await TokenManager().fetch_user(token)
            except Exception as e:
                raise BaseError(
                    error_code=ErrorCodes.INTERNAL_AUTHENTICATION_ERROR,
                    message="There was an error validating your token."
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
        except jwt_errors.ExpiredSignatureError as e:
            raise BaseError(
                error_code=ErrorCodes.USER_SESSION_EXPIRED_ERROR,
                message="The provided token is expired."
            )
        except Exception as e:
            raise e

    def _handle_authentication_exception(self, request: Request, error: BaseError) -> None:
        get_logger().error(
            error.error_code.value,
            payload={
                "request_id": request.state.request_id,
                "path": request.url.path,
                "method": request.method,
                "status_code": error.error_code.status_code or 401,
                "error": error.error_code.value,
                "detail": error.message,
                "timestamp": int(time.time()),
            }
        )
        error_details = {
            "request_id": request.state.request_id,
            "path": request.url.path,
            "method": request.method,
            "status_code": error.error_code.status_code or 401,
            "error": error.error_code.value,
            "detail": error.message,
            "timestamp": int(time.time()),
        }
        return JSONResponse(
            status_code=error_details["status_code"],
            content=error_details,
        )
