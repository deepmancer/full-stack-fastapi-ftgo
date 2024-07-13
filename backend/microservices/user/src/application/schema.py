from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError

from ftgo_utils.enums import Roles, Gender
from ftgo_utils.validators import validate_phone_number, validate_enum_value


class BaseSchema(BaseModel):    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, populate_by_name=True)

class RegisterRequest(BaseSchema):
    first_name: str = Field(..., min_length=3, max_length=30)
    last_name: str = Field(..., min_length=3, max_length=30)
    phone_number: str = Field(..., min_length=10, max_length=14)
    password: str = Field(..., min_length=8, max_length=30)
    role: str = Field(..., min_length=1, max_length=50)
    national_id: Optional[str] = Field(None, min_length=1, max_length=20)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)
    
    @field_validator('role', mode='before')
    def validate_role_field(cls, value):
        return validate_enum_value(value, Roles, 'role')
class RegisterResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    auth_code: str = Field(..., min_length=1, max_length=10)

class AuthenticateAccountResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = Field(..., min_length=1, max_length=36)

class LoginRequest(BaseSchema):
    phone_number: str = Field(..., min_length=1, max_length=15)
    role: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('role', mode='before')
    def validate_role_field(cls, value):
        return validate_enum_value(value, Roles, 'role')

class LoginResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    success: bool = Field(...)

class GetUserInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class GetUserInfoResponse(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    hashed_password: str = Field(..., min_length=1, max_length=128)
    phone_number: str = Field(..., min_length=1, max_length=15)
    gender: str = Field(..., min_length=1, max_length=10)
    role: str = Field(..., min_length=1, max_length=50)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('role', mode='before')
    def validate_role_field(cls, value):
        return validate_enum_value(value, Roles, 'role')

class AddressInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
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

class AllAddressesResponse(BaseSchema):
    addresses: list[AddressInfoResponse] = Field(...)

class AddAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)

class AddressResponse(BaseSchema):
    success: bool = Field(...)
    address_id: Optional[str] = Field(None, min_length=1, max_length=36)

class DeleteAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteAddressResponse(BaseSchema):
    success: bool = Field(...)
    address_id: str = Field(..., min_length=1, max_length=36)

class SetPreferredAddressRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    address_id: str = Field(..., min_length=1, max_length=36)

class SetPreferredAddressResponse(BaseSchema):
    success: bool = Field(...)
    address_id: str = Field(..., min_length=1, max_length=36)

class DeleteProfileRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteProfileResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteAllAddressesRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class DeleteAllAddressesResponse(BaseSchema):
    success: bool = Field(...)
    address_ids: list[str] = Field(...)

class LogoutRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class LogoutResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = Field(..., min_length=1, max_length=36)

class UpdateUserInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=14)
    gender: Optional[str] = Field(None, min_length=1, max_length=10)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('gender', mode='before')
    def validate_gender_field(cls, value):
        return validate_enum_value(value, Gender, 'gender')

class UpdateUserInfoResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = Field(..., min_length=1, max_length=36)

class ChangePasswordRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    old_password: str = Field(..., min_length=8, max_length=30)
    new_password: str = Field(..., min_length=8, max_length=30)

class ChangePasswordResponse(BaseSchema):
    success: bool = Field(...)
    user_id: str = Field(..., min_length=1, max_length=36)

class SubmitVehicleRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)
    plate_number: str = Field(..., min_length=1, max_length=20)
    license_number: str = Field(..., min_length=1, max_length=20)

class SubmitVehicleResponse(BaseSchema):
    success: bool = Field(...)
    vehicle_id: str = Field(..., min_length=1, max_length=36)

class GetVehicleInfoRequest(BaseSchema):
    user_id: str = Field(..., min_length=1, max_length=36)

class GetVehicleInfoResponse(BaseSchema):
    vehicle_id: str = Field(..., min_length=1, max_length=36)
    plate_number: str = Field(..., min_length=1, max_length=20)
    license_number: str = Field(..., min_length=1, max_length=20)

class BaseResponse(BaseSchema):
    success: bool = Field(...)
    message: str = Field(..., min_length=1, max_length=100)
