from domain.user import UserService
from application.schemas.user import (
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

class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, request: RegisterRequest) -> RegisterResponse:
        auth_code = await self.user_service.register(
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            password=request.password,
        )
        return RegisterResponse(auth_code=auth_code)

    async def authenticate_phone_number(self, request: AuthenticatePhoneNumberRequest) -> AuthenticatePhoneNumberResponse:
        success = await self.user_service.authenticate_phone_number(
            request.phone_number, request.auth_code
        )
        return AuthenticatePhoneNumberResponse(success=success)

    async def login(self, request: LoginRequest) -> LoginResponse:
        token = await self.user_service.login(
            request.phone_number, request.password
        )
        return LoginResponse(token=token)

    async def get_user_info(self, request: GetUserInfoRequest) -> GetUserInfoResponse:
        user_info = await self.user_service.get_user_info(request.user_id)
        return GetUserInfoResponse(**user_info)

    async def add_address(self, request: AddAddressRequest) -> AddressResponse:
        address_id, success = await self.user_service.add_address(
            request.user_id, request.address_line_1, request.address_line_2,
            request.city, request.state, request.postal_code, request.country
        )
        return AddressResponse(id=address_id, success=success)

    async def modify_address(self, request: ModifyAddressRequest) -> AddressResponse:
        success = await self.user_service.modify_address(
            request.address_id, request.address_line_1, request.address_line_2,
            request.city, request.state, request.postal_code, request.country
        )
        return AddressResponse(success=success)

    async def delete_address(self, request: DeleteAddressRequest) -> AddressResponse:
        success = await self.user_service.delete_address(request.address_id)
        return AddressResponse(success=success)
    
    async def set_preferred_address(self, request: SetPreferredAddressRequest) -> AddressResponse:
        success = await self.user_service.set_preferred_address(request.address_id)
        return AddressResponse(success=success)
    
    async def delete_account(self, request: DeleteAccountRequest) -> DeleteAccountResponse:
        success = await self.user_service.delete_account(request.user_id)
        return DeleteAccountResponse(success=success)
    
    async def delete_all_addresses(self, request: DeleteAllAddressesRequest) -> DeleteAllAddressesResponse:
        success = await self.user_service.delete_all_addresses(request.user_id)
        return DeleteAllAddressesResponse(success=success)