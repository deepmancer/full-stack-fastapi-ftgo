from pydantic import BaseModel, Field, validator, BaseConfig
from utils.validators import validate_password, validate_phone_number, validate_enum
from config.enums import RoleName

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
    role_name: str = Field(..., min_length=1, max_length=50)

    @validator('password')
    def validate_password_field(cls, value):
        return validate_password(value)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @validator('role_name')
    def validate_role_name_field(cls, value):
        return validate_enum(value, RoleName)

class RegisterResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountResponse(BaseSchema):
    access_token: str = Field(..., min_length=1, max_length=100)
    access_token_ttl_seconds: int = Field(..., ge=1)

class LoginRequest(BaseSchema):
    phone_number: str = Field(..., min_length=1, max_length=15)
    role_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def validate_password_field(cls, value):
        return validate_password(value)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @validator('role_name')
    def validate_role_name_field(cls, value):
        return validate_enum(value, RoleName)

class LoginResponse(BaseSchema):
    access_token: str
    access_token_ttl_seconds: int = Field(..., ge=1)

class GetUserInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class GetUserInfoResponse(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=15)
    gender: str = Field(..., min_length=1, max_length=10)
    role_name: str = Field(..., min_length=1, max_length=50)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @validator('role_name')
    def validate_role_name_field(cls, value):
        return validate_enum(value, RoleName)

class AddAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=50)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=50)

class AddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteAddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)
    success: bool

class SetPreferredAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    address_id: str = Field(..., min_length=1, max_length=36)

class SetPreferredAddressResponse(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)
    success: bool
class DeleteAccountRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteAccountResponse(BaseSchema):
    success: bool

class DeleteAllAddressesRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteAllAddressesResponse(BaseSchema):
    address_ids: list[str] = Field(...)
    success: bool
