from typing import Optional, Dict
from pydantic import Field

from schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, BaseSchema, uuid_field,
    UserInfoMixin
)

class RegisterRequest(UserInfoMixin):
    password: str = Field(..., min_length=8, max_length=30)

class RegisterResponse(BaseSchema):
    user_id: str = uuid_field()
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountRequest(BaseSchema):
    user_id: str = uuid_field()
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = uuid_field()

class LoginRequest(BaseSchema, PhoneNumberMixin, RoleMixin):
    password: str = Field(..., min_length=8, max_length=128)

class LoginResponse(BaseSchema):
    user_id: str = uuid_field()
    success: bool = Field(...)

class GetUserInfoRequest(BaseSchema):
    user_id: str = uuid_field()

class GetUserInfoResponse(UserInfoMixin):
    pass

class DeleteProfileRequest(BaseSchema):
    user_id: str = uuid_field()

class DeleteProfileResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = uuid_field()

class LogoutRequest(BaseSchema):
    user_id: str = uuid_field()

class LogoutResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = uuid_field()

class ChangePasswordRequest(BaseSchema):
    user_id: str = uuid_field()
    old_password: str = Field(..., min_length=8, max_length=30)
    new_password: str = Field(..., min_length=8, max_length=30)

class ChangePasswordResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = uuid_field()

class UpdateProfileRequest(BaseSchema):
    user_id: str = uuid_field()
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[str] = Field(None, min_length=1, max_length=10)

class UpdateProfileResponse(UserMixin):
    success: bool = Field(...)

class GetUserWithCredentialsRequest(BaseSchema):
    user_id: str = uuid_field()
    
class GetUserWithCredentialsResponse(UserMixin):
    hashed_password: Optional[str] = Field(None, min_length=1, max_length=128)
