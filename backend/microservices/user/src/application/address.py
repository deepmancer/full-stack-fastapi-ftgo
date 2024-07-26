from typing import Dict, Any

from domain.user import UserDomain

class AddressService:
    """
    Service class for managing user addresses.
    """

    @staticmethod
    async def add_address(
        user_id: str,
        address_line_1: str,
        address_line_2: str,
        city: str,
        postal_code: str,
        country: str
    ) -> Dict[str, Any]:
        """
        Adds a new address to the user's account.

        :param user_id: ID of the user.
        :param address_line_1: First line of the address.
        :param address_line_2: Second line of the address.
        :param city: City of the address.
        :param postal_code: Postal code of the address.
        :param country: Country of the address.
        :return: Dictionary containing status and address information.
        """
        user = await UserDomain.load(user_id)
        address_info = await user.add_address(
            address_line_1, address_line_2, city, postal_code, country
        )
        return address_info

    @staticmethod
    async def get_default_address(user_id: str) -> Dict[str, Any]:
        """
        Retrieves the default address of the user.

        :param user_id: ID of the user.
        :return: Dictionary containing status and default address information.
        """
        user = await UserDomain.load(user_id)
        address_info = await user.get_default_address()
        return address_info

    @staticmethod
    async def delete_address(user_id: str, address_id: str) -> Dict[str, Any]:
        """
        Deletes an address from the user's account.

        :param user_id: ID of the user.
        :param address_id: ID of the address to be deleted.
        :return: Dictionary containing status and address ID.
        """
        user = await UserDomain.load(user_id)
        await user.delete_address(address_id)
        return {
            "address_id": address_id,
        }

    @staticmethod
    async def set_preferred_address(user_id: str, address_id: str) -> Dict[str, Any]:
        """
        Sets or unsets an address as the user's default address.

        :param user_id: ID of the user.
        :param address_id: ID of the address to be set or unset as default.
        :param set_default: Boolean indicating whether to set or unset the address as default.
        :return: Dictionary containing status, address ID, and default status.
        """
        user = await UserDomain.load(user_id)

        await user.set_address_as_default(address_id)
        return {
            "address_id": address_id,
        }

    @staticmethod
    async def get_address_info(user_id: str, address_id: str) -> Dict[str, Any]:
        """
        Retrieves information about a specific address.

        :param user_id: ID of the user.
        :param address_id: ID of the address.
        :return: Dictionary containing status and address information.
        """
        user = await UserDomain.load(user_id)
        address_info = await user.get_address_info(address_id)
        return address_info

    @staticmethod
    async def get_all_addresses(user_id: str) -> Dict[str, Any]:
        """
        Retrieves all addresses associated with the user's account.

        :param user_id: ID of the user.
        :return: Dictionary containing status and a list of addresses.
        """
        user = await UserDomain.load(user_id)
        addresses = await user.get_addresses_info()
        return {
            "addresses": addresses,
        }

    @staticmethod
    async def update_address(
        user_id: str,
        address_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates information for a specific address.

        :param user_id: ID of the user.
        :param address_id: ID of the address to be updated.
        :param update_data: Dictionary containing the updated address information.
        :return: Dictionary containing status and updated address information.
        """
        user = await UserDomain.load(user_id)
        address_info = await user.update_address_information(
            address_id, update_data
        )
        return address_info
