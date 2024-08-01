from enum import Enum
from fastapi import Depends, Request, status
from typing import List, Union

from ftgo_utils.errors import BaseError, ErrorCodes

from application.schemas.user import UserStateSchema

class AccessManager:
    def __init__(self, allowed_roles: List[Union[str, Enum]]) -> None:
        self.allowed_roles = [role.value if isinstance(role, Enum) else role for role in allowed_roles]

    def __call__(self, request: Request) -> None:
        if not hasattr(request.state, "user") or request.state.user is None:
            return

        user: UserStateSchema = request.state.user
        if user.role not in self.allowed_roles:
            raise BaseError(
                error_code=ErrorCodes.USER_PERMISSION_DENIED_ERROR,
                status_code=status.HTTP_403_FORBIDDEN,
                message=f"Access forbidden: Only roles of [{', '.join(self.allowed_roles)}] are allowed",
                issuer=self.__class__.__name__,
            )
