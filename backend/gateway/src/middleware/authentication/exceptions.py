from typing import Any

from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from config.exceptions import UserAuthenticationError

class MissingAuthorizationHeader(UserAuthenticationError):
    def __init__(self):
        super().__init__("Authorization header is missing")


class InvalidAuthorizationScheme(UserAuthenticationError):
    def __init__(self, scheme: str):
        super().__init__(f"Authorization scheme '{scheme}' is not supported")


class InvalidToken(UserAuthenticationError):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(detail)


class TokenNotFound(UserAuthenticationError):
    def __init__(self):
        super().__init__("Token not found")


class IdentityMismatch(UserAuthenticationError):
    def __init__(self):
        super().__init__("Identity mismatch")


class TokenDecodingError(UserAuthenticationError):
    def __init__(self):
        super().__init__("Token decoding failed or payload is empty")


class UserValidationError(UserAuthenticationError):
    def __init__(self, errors: Any):
        super().__init__(f"User validation error: {errors}", status_code=HTTP_400_BAD_REQUEST)


class InternalAuthenticationError(UserAuthenticationError):
    def __init__(self, detail: str):
        super().__init__(detail, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
