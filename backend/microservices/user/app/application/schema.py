from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from config.enums import Roles
from typing import Optional
from application.validators import validate_password, validate_phone_number, validate_role, validate_uuid


class BaseSchema(BaseModel):    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, populate_by_name=True)

class RegisterRequest(BaseSchema):
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
    
class RegisterResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)
    
    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class AuthenticateAccountRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class AuthenticateAccountResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class LoginRequest(BaseSchema):
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

class LoginResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class GetUserInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class GetUserInfoResponse(BaseSchema):
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

class AddressInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)
    
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

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

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

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class AddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class DeleteAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class DeleteAddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)
    
class SetPreferredAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class SetPreferredAddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('address_id', mode='before')
    def validate_address_id_field(cls, value):
        return validate_uuid(value)

class DeleteProfileRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class DeleteProfileResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class DeleteAllAddressesRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class DeleteAllAddressesResponse(BaseSchema):
    address_ids: list[str] = Field(...)

    @field_validator('address_ids', mode='before')
    def validate_address_ids_field(cls, value):
        return [validate_uuid(v) for v in value]

class LogoutRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    access_token: str = Field(..., min_length=1, max_length=200)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)

class LogoutResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('user_id', mode='before')
    def validate_user_id_field(cls, value):
        return validate_uuid(value)
