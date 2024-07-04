from application.schemas.base import BaseSchema

class RegisterRequest(BaseSchema):
    first_name: str
    last_name: str
    phone_number: str
    password: str

class RegisterResponse(BaseSchema):
    auth_code: str

class AuthenticatePhoneNumberRequest(BaseSchema):
    phone_number: str
    auth_code: str

class AuthenticatePhoneNumberResponse(BaseSchema):
    success: bool

class LoginRequest(BaseSchema):
    phone_number: str
    password: str

class LoginResponse(BaseSchema):
    token: str

class GetUserInfoRequest(BaseSchema):
    user_id: str

class GetUserInfoResponse(BaseSchema):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    phone_number_verified: bool
    gender: str
    created_at: str
    updated_at: str

class AddAddressRequest(BaseSchema):
    user_id: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    postal_code: str
    country: str

class AddressResponse(BaseSchema):
    id: str
    success: bool

class ModifyAddressRequest(BaseSchema):
    address_id: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    postal_code: str
    country: str

class DeleteAddressRequest(BaseSchema):
    address_id: str

class SetPreferredAddressRequest(BaseSchema):
    address_id: str

class DeleteAccountRequest(BaseSchema):
    user_id: str

class DeleteAccountResponse(BaseSchema):
    success: bool

class DeleteAllAddressesRequest(BaseSchema):
    user_id: str

class DeleteAllAddressesResponse(BaseSchema):
    success: bool
