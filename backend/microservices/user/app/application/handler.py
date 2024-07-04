from application.schemas.base import (
    RegisterRequest, RegisterResponse,
    AuthenticatePhoneNumberRequest, AuthenticatePhoneNumberResponse,
    LoginRequest, LoginResponse,
    GetUserInfoRequest, GetUserInfoResponse,
    AddAddressRequest, AddressResponse,
    ModifyAddressRequest,
    DeleteAddressRequest,
    SetPreferredAddressRequest,
    DeleteAccountRequest, DeleteAccountResponse,
    DeleteAllAddressesRequest, DeleteAllAddressesResponse
)
from domain.services.user_service import UserDomain

class UserHandler:

    async def register(self, request: RegisterRequest) -> RegisterResponse:
        auth_code = await UserDomain.register(
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            password=request.password,
        )
        return RegisterResponse(auth_code=auth_code)

    async def authenticate_phone_number(self, request: AuthenticatePhoneNumberRequest) -> AuthenticatePhoneNumberResponse:
        user_service = await UserDomain.from_user_id(request.phone_number)
        success = await user_service.authenticate_phone_number(request.auth_code)
        return AuthenticatePhoneNumberResponse(success=success)

    async def login(self, request: LoginRequest) -> LoginResponse:
        user_service = await UserDomain.from_user_id(request.phone_number)
        token = await user_service.login(request.password)
        return LoginResponse(token=token)

    async def get_user_info(self, request: GetUserInfoRequest) -> GetUserInfoResponse:
        user_service = await UserDomain.from_user_id(request.user_id)
        user_info = await user_service.get_user_info()
        return GetUserInfoResponse(**user_info)

    async def add_address(self, request: AddAddressRequest) -> AddressResponse:
        user_service = await UserDomain.from_user_id(request.user_id)
        address_id = await user_service.add_address(
            request.address_line_1, request.address_line_2,
            request.city, request.state, request.postal_code, request.country
        )
        return AddressResponse(id=address_id, success=True)

    async def modify_address(self, request: ModifyAddressRequest) -> AddressResponse:
        user_service = await UserDomain.from_user_id(request.user_id)
        success = await user_service.modify_address(
            request.address_id, request.address_line_1, request.address_line_2,
            request.city, request.state, request.postal_code, request.country
        )
        return AddressResponse(id=request.address_id, success=success)

    async def delete_address(self, request: DeleteAddressRequest) -> AddressResponse:
        user_service = await UserDomain.from_user_id(request.user_id)
        success = await user_service.delete_address(request.address_id)
        return AddressResponse(id=request.address_id, success=success)
    
    async def set_preferred_address(self, request: SetPreferredAddressRequest) -> AddressResponse:
        user_service = await UserDomain.from_user_id(request.user_id)
        success = await user_service.set_preferred_address(request.address_id)
        return AddressResponse(id=request.address_id, success=success)
    
    async def delete_account(self, request: DeleteAccountRequest) -> DeleteAccountResponse:
        user_service = await UserDomain.from_user_id(request.user_id)
        success = await user_service.delete_account()
        return DeleteAccountResponse(success=success)
    
    async def delete_all_addresses(self, request: DeleteAllAddressesRequest) -> DeleteAllAddressesResponse:
        user_service = await UserDomain.from_user_id(request.user_id)
        success = await user_service.delete_all_addresses()
        return DeleteAllAddressesResponse(success=success)
