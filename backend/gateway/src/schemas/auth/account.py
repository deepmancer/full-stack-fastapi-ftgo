from typing import Optional, Dict
from pydantic import Field

from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, BaseSchema, UserInfoMixin, LocationMixin, uuid_field, 
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
    user_id: str = uuid_field()

class LoginRequest(PhoneNumberMixin, RoleMixin):
    password: str = Field(..., min_length=8, max_length=128)

class LoginResponse(BaseSchema):
    user_id: str = uuid_field()

class GetUserInfoRequest(BaseSchema):
    user_id: str = uuid_field()

class GetUserInfoResponse(UserInfoMixin):
    pass

class DeleteProfileRequest(BaseSchema):
    user_id: str = uuid_field()

class DeleteProfileResponse(BaseSchema):
    user_id: str = uuid_field()

class LogoutRequest(BaseSchema):
    user_id: str = uuid_field()

class LogoutResponse(BaseSchema):
    user_id: str = uuid_field()

class ChangePasswordRequest(BaseSchema):
    user_id: str = uuid_field()
    old_password: str = Field(..., min_length=8, max_length=30)
    new_password: str = Field(..., min_length=8, max_length=30)

class ChangePasswordResponse(BaseSchema):
    user_id: str = uuid_field()

class UpdateProfileRequest(BaseSchema):
    user_id: str = uuid_field()
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[str] = Field(None, min_length=1, max_length=10)

class UpdateProfileResponse(UserMixin):
    pass
class GetUserWithCredentialsRequest(BaseSchema):
    user_id: str = uuid_field()
    
class GetUserWithCredentialsResponse(UserMixin):
    hashed_password: Optional[str] = Field(None, min_length=1, max_length=128)
