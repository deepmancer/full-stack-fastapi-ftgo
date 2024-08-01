from typing import Dict, Any, Optional

from domain import UserManager

class AddressService:
    @staticmethod
    async def add_address(
        user_id: str,
        latitude: float,
        longitude: float,
        address_line_1: str,
        address_line_2: str,
        city: str,
        postal_code: Optional[str] = None,
        country: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        
        user = await UserManager.load(user_id=user_id)
        address_info = await user.add_address(
            latitude=latitude,
            longitude=longitude,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            postal_code=postal_code,
            country=country,
        )
        return address_info

    @staticmethod
    async def get_default_address(user_id: str, **kwargs) -> Dict[str, Any]:
        user = await UserManager.load(user_id)
        address_info = await user.get_default_address_info()
        return address_info

    @staticmethod
    async def delete_address(user_id: str, address_id: str, **kwargs) -> Dict[str, Any]:
        user = await UserManager.load(user_id)
        await user.delete_address(address_id)
        return {}

    @staticmethod
    async def set_preferred_address(user_id: str, address_id: str, **kwargs) -> Dict[str, Any]:
        user = await UserManager.load(user_id)
        updated_address_info = await user.set_address_as_default(address_id)
        return updated_address_info

    @staticmethod
    async def get_address_info(user_id: str, address_id: str, **kwargs) -> Dict[str, Any]:
        user = await UserManager.load(user_id)
        address_info = await user.get_address_info(address_id)
        return address_info

    @staticmethod
    async def get_all_addresses(user_id: str, **kwargs) -> Dict[str, Any]:
        user = await UserManager.load(user_id)
        addresses = user.get_addresses_info()
        return {
            "addresses": addresses,
        }

    @staticmethod
    async def update_information(
        user_id: str,
        address_id: str,
        update_data: Dict[str, Any],
        **kwargs,
    ) -> Dict[str, Any]:
        user = await UserManager.load(user_id)
        updated_address_info = await user.update_address_information(
            address_id, update_data,
        )
        return updated_address_info
