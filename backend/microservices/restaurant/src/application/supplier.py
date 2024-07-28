from typing import Dict, Any
import json
from application import get_logger
from domain.restaurant import RestaurantDomain

class RestaurantService:
    """
    Service class for managing restaurant profiles.
    """

    @staticmethod
    async def register(
        owner_user_id: str,
        name: str,
        postal_code: str,
        address: str,
        address_lat: float,
        address_lng: float,
        restaurant_licence_id: str,
    ) -> Dict[str, Any]:
        """
        Registers a new restaurant.

        :param owner_user_id: id of the restaurant owner.
        :param name: Name of the restaurant.
        :param postal_code: Postal Code of the restaurant.
        :param address: Address of the restaurant.
        :param address_lat: Address's latitude.
        :param address_lng: Address's longitude.
        :param restaurant_licence_id: Licence ID of the restaurant.
        :return: Dictionary containing restaurant ID.
        """
        restaurant_id = await RestaurantDomain.register(
            owner_user_id=owner_user_id,
            name=name,
            postal_code=postal_code,
            address=address,
            address_lat=address_lat,
            address_lng=address_lng,
            restaurant_licence_id=restaurant_licence_id,
        )
        return {
            "restaurant_id": restaurant_id
        }

    @staticmethod
    async def get_restaurant_info(restaurant_id: str) -> Dict[str, Any]:
        """
        Retrieves restaurant information.

        :param restaurant_id: ID of the restaurant.
        :return: Dictionary containing restaurant information.
        """
        restaurant = await RestaurantDomain.load(restaurant_id=restaurant_id)
        return restaurant.get_info()

    @staticmethod
    async def get_supplier_restaurant_info(user_id: str) -> Dict[str, Any]:
        """
        Retrieves restaurant information.

        :param user_id: ID of the restaurant's owner.
        :return: Dictionary containing restaurant information.
        """
        restaurant = await RestaurantDomain.load(owner_user_id=user_id)
        return restaurant.get_info()

    @staticmethod
    async def update_information(restaurant_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates restaurant profile information.

        :param restaurant_id: ID of the restaurant.
        :param update_data: Dictionary containing the updated restaurant information.
        :return: Dictionary containing updated restaurant information.
        """
        restaurant = await RestaurantDomain.load(restaurant_id=restaurant_id)
        return await restaurant.update_profile_information(update_data)

    @staticmethod
    async def delete_restaurant(restaurant_id: str) -> Dict[str, str]:
        """
        Deletes a restaurant account.

        :param restaurant_id: ID of the restaurant.
        :return: Dictionary containing restaurant ID.
        """
        restaurant = await RestaurantDomain.load(restaurant_id=restaurant_id)
        await restaurant.delete_restaurant()
        return {
            "restaurant_id": restaurant_id,
        }
