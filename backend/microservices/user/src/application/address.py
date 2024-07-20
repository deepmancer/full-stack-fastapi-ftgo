from application.interfaces.address import *
from domain.user import UserDomain

class AddressService:

    @staticmethod
    async def add_address(request: AddAddressRequest) -> AddAddressResponse:
        user = await UserDomain.load(request.user_id)
        address_info = await user.add_address(
            request.address_line_1, request.address_line_2, request.city, request.postal_code, request.country
        )
        return AddAddressResponse(
            success=True,
            **address_info,
        )

    @staticmethod
    async def get_default_address(request: GetDefaultAddressRequest) -> AddressInfoResponse:
        user = await UserDomain.load(request.user_id)
        address_info = await user.get_default_address()
        return AddressInfoResponse(**address_info)

    @staticmethod
    async def delete_address(request: DeleteAddressRequest) -> DeleteAddressResponse:
        user = await UserDomain.load(request.user_id)
        await user.delete_address(request.address_id)
        return DeleteAddressResponse(address_id=request.address_id, success=True)

    @staticmethod
    async def set_preferred_address(request: SetPreferredAddressRequest) -> SetPreferredAddressResponse:
        user = await UserDomain.load(request.user_id)
        set_default = request.set_default
        if set_default:
            await user.set_address_as_default(request.address_id)
        else:
            await user.unset_address_as_default(request.address_id)
        return SetPreferredAddressResponse(address_id=request.address_id, is_default=set_default, success=True)

    @staticmethod
    async def get_address_info(request: AddressInfoRequest) -> AddressInfoResponse:
        user = await UserDomain.load(request.user_id)
        address_info = await user.get_address_info(request.address_id)
        return AddressInfoResponse(**address_info)

    @staticmethod
    async def get_all_addresses(request: AllAddressesRequest) -> AllAddressesResponse:
        user = await UserDomain.load(request.user_id)
        addresses = await user.get_addresses_info()
        return AllAddressesResponse(addresses=addresses)

    @staticmethod
    async def update_address(request: UpdateAddressRequest) -> UpdateAddressResponse:
        user = await UserDomain.load(request.user_id)
        address_info = await user.update_address_information(
            request.address_id, request.dict(exclude={"user_id", "address_id"}),
        )
        return UpdateAddressResponse(success=True, **address_info)
