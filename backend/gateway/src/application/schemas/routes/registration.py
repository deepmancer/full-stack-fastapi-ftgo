from typing import Optional
from pydantic import BaseModel, Field
from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, UserInfoMixin, uuid_field,
)

class RegisterSchema(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=30)
    last_name: str = Field(..., min_length=3, max_length=30)
    phone_number: str = Field(..., min_length=10, max_length=14)
    password: str = Field(..., min_length=8, max_length=30)
    role: str = Field(..., min_length=1, max_length=50)
    national_id: Optional[str] = Field(None, min_length=1, max_length=20)

class UserIdSchema(BaseModel):
    user_id: str = uuid_field()
    auth_code: str = Field(..., min_length=1, max_length=100)

class AuthenticateAccountSchema(BaseModel):
    user_id: str = uuid_field()
    auth_code: str = Field(..., min_length=1, max_length=100)

class UserIdVerifiedSchema(BaseModel):
    success: bool = Field(...)

class AuthCodeSchema(BaseModel):
    auth_code: str = Field(..., min_length=1, max_length=100)

class LoginSchema(BaseModel):
    phone_number: str = Field(..., min_length=1, max_length=15)
    role: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

class TokenSchema(BaseModel):
    user_id: str = uuid_field()
    auth_code: str = Field(..., min_length=1, max_length=100)

class LogoutResponse(BaseModel):
    user_id: str = uuid_field()

class GetUserInfoResponse(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=30)
    last_name: str = Field(..., min_length=3, max_length=30)
    phone_number: str = Field(..., min_length=10, max_length=14)
    national_id: Optional[str] = Field(None, min_length=1, max_length=20)


class DeleteProfileResponse(BaseModel):
    success: bool = Field(...)

class ChangePasswordSchema(BaseModel):
    user_id: str = uuid_field()
    old_password: str = Field(..., min_length=8, max_length=30)
    new_password: str = Field(..., min_length=8, max_length=30)

class UpdateProfileSchema(BaseModel):
    user_id: str = uuid_field()
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[str] = Field(None, min_length=1, max_length=10)

class UserWithCredentialsSchema(UserMixin):
    hashed_password: Optional[str] = Field(None, min_length=1, max_length=128)
