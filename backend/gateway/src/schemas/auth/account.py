from pydantic import Field, field_validator, ConfigDict, ValidationError
from config.enums import Roles
from typing import Optional
from utils.validators import validate_password, validate_phone_number, validate_role, validate_uuid
from schemas.base import BaseModel


class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=30)
    last_name: str = Field(..., min_length=3, max_length=30)
    phone_number: str = Field(..., min_length=10, max_length=14)
    password: str = Field(..., min_length=8, max_length=30)
    role: str = Field(..., min_length=1, max_length=50)
    national_id: Optional[str] = Field(None, min_length=1, max_length=20)

    @field_validator('password', mode='before')
    def validate_password_field(cls, value):
        return validate_password(value)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)
    
    @field_validator('role', mode='before')
    def validate_role_field(cls, value):
        return validate_role(value)
    
class RegisterResponse(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)
    
    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class AuthenticateAccountRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class AuthenticateAccountResponse(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class LoginRequest(BaseModel):
    phone_number: str = Field(..., min_length=1, max_length=15)
    role: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password', mode='before')
    def validate_password_field(cls, value):
        return validate_password(value)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('role', mode='before')
    def validate_role_field(cls, value):
        return validate_role(value)

class LoginResponse(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class GetUserInfoRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class GetUserInfoResponse(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=15)
    gender: str = Field(..., min_length=1, max_length=10)
    role: str = Field(..., min_length=1, max_length=50)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('role', mode='before')
    def validate_role_field(cls, value):
        return validate_role(value)

class AddressInfoRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)
    
class AddressInfoResponse(BaseModel):
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    is_default: bool = Field(...)

class AllAddressesRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class AllAddressesResponse(BaseModel):
    addresses: list[AddressInfoResponse] = Field(...)

class AddAddressRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class AddressResponse(BaseModel):
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class DeleteAddressRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class DeleteAddressResponse(BaseModel):
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)
    
class SetPreferredAddressRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class SetPreferredAddressResponse(BaseModel):
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class DeleteProfileRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class DeleteProfileResponse(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class DeleteAllAddressesRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class DeleteAllAddressesResponse(BaseModel):
    address_ids: list[str] = Field(...)

    @field_validator('address_ids', mode='before')
    def validate_address_ids_field(cls, value):
        return [validate_uuid(v) for v in value]

class LogoutRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class LogoutResponse(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)
