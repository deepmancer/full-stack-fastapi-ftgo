from typing import Optional
from pydantic import BaseModel, Field
from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, UserInfoMixin, uuid_field,
)

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
