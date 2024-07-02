from domain.user import UserService
from grpc_interface.user_service_pb2 import (
    RegisterRequest, RegisterResponse,
    AuthenticatePhoneNumberRequest, AuthenticatePhoneNumberResponse,
    LoginRequest, LoginResponse,
    GetUserInfoRequest, GetUserInfoResponse,
    AddAddressRequest, AddressResponse,
    ModifyAddressRequest,
    DeleteAddressRequest,
    SetPreferredAddressRequest
)

class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def Register(self, request: RegisterRequest, context) -> RegisterResponse:
        auth_code = await self.user_service.register(
            request.first_name, request.last_name, request.phone_number, request.password
        )
        return RegisterResponse(auth_code=auth_code)

    async def AuthenticatePhoneNumber(self, request: AuthenticatePhoneNumberRequest, context) -> AuthenticatePhoneNumberResponse:
        success = await self.user_service.authenticate_phone_number(
            request.phone_number, request.auth_code
        )
        return AuthenticatePhoneNumberResponse(success=success)

    async def Login(self, request: LoginRequest, context) -> LoginResponse:
        token = await self.user_service.login(
            request.phone_number, request.password
        )
        return LoginResponse(token=token)

    async def GetUserInfo(self, request: GetUserInfoRequest, context) -> GetUserInfoResponse:
        user_info = await self.user_service.get_user_info(request.user_id)
        return GetUserInfoResponse(**user_info)

    async def AddAddress(self, request: AddAddressRequest, context) -> AddressResponse:
        address_id, success = await self.user_service.add_address(
            request.user_id, request.address_line_1, request.address_line_2,
            request.city, request.state, request.postal_code, request.country
        )
        return AddressResponse(id=address_id, success=success)

    async def ModifyAddress(self, request: ModifyAddressRequest, context) -> AddressResponse:
        success = await self.user_service.modify_address(
            request.address_id, request.address_line_1, request.address_line_2,
            request.city, request.state, request.postal_code, request.country
        )
        return AddressResponse(success=success)

    async def DeleteAddress(self, request: DeleteAddressRequest, context) -> AddressResponse:
        success = await self.user_service.delete_address(request.address_id)
        return AddressResponse(success=success)

    async def SetPreferredAddress(self, request: SetPreferredAddressRequest, context) -> AddressResponse:
        success = await self.user_service.set_preferred_address(request.address_id)
        return AddressResponse(success=success)
