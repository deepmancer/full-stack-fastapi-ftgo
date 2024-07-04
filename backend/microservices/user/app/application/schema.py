from pydantic import BaseModel, Field, validator, BaseConfig
from utils.validators import validate_password, validate_phone_number, validate_email


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        orm_mode: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True

class RegisterRequest(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=15)
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def validate_password_field(cls, value):
        return validate_password(value)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

class RegisterResponse(BaseSchema):
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticatePhoneNumberRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    phone_number: str = Field(..., min_length=1, max_length=15)
    auth_code: str = Field(..., min_length=1, max_length=10)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

class AuthenticatePhoneNumberResponse(BaseSchema):
    success: bool

class LoginRequest(BaseSchema):
    phone_number: str = Field(..., min_length=1, max_length=15)
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def validate_password_field(cls, value):
        return validate_password(value)

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

class LoginResponse(BaseSchema):
    token: str

class GetUserInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class GetUserInfoResponse(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=15)
    email: str = Field(..., min_length=1, max_length=100)
    phone_number_verified: bool
    gender: str = Field(..., min_length=1, max_length=10)
    created_at: str
    updated_at: str

    @validator('phone_number')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @validator('email')
    def validate_email_field(cls, value):
        return validate_email(value)

class AddAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=50)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=50)

class AddressResponse(BaseSchema):
    id: str = Field(..., min_length=1, max_length=36)
    success: bool

class ModifyAddressRequest(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=50)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=50)

class DeleteAddressRequest(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

class SetPreferredAddressRequest(BaseSchema):
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteAccountRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteAccountResponse(BaseSchema):
    success: bool

class DeleteAllAddressesRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteAllAddressesResponse(BaseSchema):
    success: bool
