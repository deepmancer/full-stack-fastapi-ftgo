from pydantic import BaseModel, Field, validator, BaseConfig
from utils.validators import validate_password, validate_phone_number, validate_enum
from config.enums import Roles
from typing import Optional

class BaseSchema(BaseModel):
    class Config(BaseConfig):
        from_attributes: bool = True
        validate_assignment: bool = True
        populate_by_name: bool = True

class RegisterRequest(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=15)
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(..., min_length=1, max_length=50)
    national_id: Optional[str] = Field(None, min_length=1, max_length=20)

    @validator('password')
    def validate_password_field(cls, value):
        return validate_password(value)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @validator('role')
    def validate_role_field(cls, value):
        return validate_enum(value, Roles)

class RegisterResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class LoginRequest(BaseSchema):
    phone_number: str = Field(..., min_length=1, max_length=15)
    role: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def validate_password_field(cls, value):
        return validate_password(value)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @validator('role')
    def validate_role_field(cls, value):
        return validate_enum(value, Roles)

class LoginResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

class GetUserInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

class GetUserInfoResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=15)
    gender: str = Field(..., min_length=1, max_length=10)
    role: str = Field(..., min_length=1, max_length=50)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @validator('role')
    def validate_role_field(cls, value):
        return validate_enum(value, Roles)

class AddressInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)
    
class AddressInfoResponse(BaseSchema):
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    is_default: bool = Field(...)

class AllAddressesRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

class AllAddressesResponse(BaseSchema):
    addresses: list[AddressInfoResponse] = Field(...)
class AddAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)

class AddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteAddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)
    
class SetPreferredAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

class SetPreferredAddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteProfileRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

class DeleteProfileResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteAllAddressesRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

class DeleteAllAddressesResponse(BaseSchema):
    address_ids: list[str] = Field(...)

class LogoutRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

class LogoutResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
