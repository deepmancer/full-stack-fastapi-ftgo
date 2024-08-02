from typing import Optional
from pydantic import BaseModel

from pydantic import Field

from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserIdMixin, GenderMixin, UserInfoMixin, UserMixin, TokenMixin
)


class RegistrationSchema(UserInfoMixin):
    password: str = Field(..., min_length=8, max_length=128)

class UserAuthCodeSchema(UserIdMixin):
    auth_code: str = Field(..., min_length=1, max_length=10)

class LoginSchema(PhoneNumberMixin, RoleMixin):
    password: str = Field(..., min_length=8, max_length=128)

class ChangePasswordSchema(UserIdMixin):
    old_password: str = Field(..., min_length=8, max_length=30)
    new_password: str = Field(..., min_length=8, max_length=30)

class UpdateProfileSchema(UserIdMixin, GenderMixin):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)

class UserInfo(UserInfoMixin):
    role: str = Field(..., min_length=1, max_length=20)


class UpdateUserRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)