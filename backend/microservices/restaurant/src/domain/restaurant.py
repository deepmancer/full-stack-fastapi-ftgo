import asyncio
from typing import Any, Dict, Optional, List

from data_access.repository import DatabaseRepository
from domain.exceptions import RestaurantExistsError, RestaurantNotFoundError
from domain import get_logger
from models.supplier import Supplier
from domain import MenuDomain
from models.menu import MenuItem

import ftgo_utils as utils

class RestaurantDomain:
    def __init__(
        self,
        restaurant_id: str,
        owner_user_id: str,
        name: str,
        postal_code: str,
        address: str,
        address_lat: float,
        address_lng: float,
        restaurant_licence_id: str,
        created_at: str,
        updated_at: Optional[str],
    ):
        self.restaurant_id = restaurant_id
        self.owner_user_id = owner_user_id
        self.name = name
        self.postal_code = postal_code
        self.address = address
        self.address_lat = address_lat
        self.address_lng = address_lng
        self.restaurant_licence_id = restaurant_licence_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.menu = None

    @classmethod
    async def load(
        cls,
        owner_user_id: Optional[str] = None,
        restaurant_id: Optional[str] = None,
    ) -> "RestaurantDomain":
        query_dict = {}
        if restaurant_id:
            query_dict["id"] = restaurant_id
        if owner_user_id:
            query_dict["owner_user_id"] = owner_user_id
        try:
            restaurant_profile = await DatabaseRepository.fetch_by_query(Supplier, query=query_dict, one_or_none=True)
            if not restaurant_profile:
                raise RestaurantNotFoundError(query_dict)

            return RestaurantDomain._from_profile(restaurant_profile)
        except Exception as e:
            get_logger().error(f"Error loading restaurant with query {query_dict}: {str(e)}")
            raise e

    @staticmethod
    async def register(
        owner_user_id: str,
        name: str,
        postal_code: str,
        address: str,
        address_lat: float,
        address_lng: float,
        restaurant_licence_id: str,
    ) -> str:
        try:
            current_records = await DatabaseRepository.fetch_by_query(Supplier, query={"owner_user_id": owner_user_id})
            if current_records:
                raise RestaurantExistsError(owner_user_id=owner_user_id)

            restaurant_id = utils.uuid_gen.uuid4()

            new_profile = Supplier(
                id=restaurant_id,
                owner_user_id=owner_user_id,
                name=name,
                postal_code=postal_code,
                address=address,
                address_lat=address_lat,
                address_lng=address_lng,
                restaurant_licence_id=restaurant_licence_id,
            )
            new_profile = await DatabaseRepository.insert(new_profile)
            return restaurant_id
        except Exception as e:
            get_logger().error(f"Error registering restaurant with owner_user_id {owner_user_id}: {str(e)}")
            raise e

    async def update_profile_information(self, update_fields: Dict[str, Optional[str]]):
        try:
            name = update_fields.get("name")
            postal_code = update_fields.get("postal_code")
            address = update_fields.get("address")
            address_lat = update_fields.get("address_lat")
            address_lng = update_fields.get("address_lng")

            new_fields = {}
            if name:
                new_fields["name"] = name
            if postal_code:
                new_fields["postal_code"] = postal_code
            if address:
                new_fields["address"] = address
            if address_lat:
                new_fields["address_lat"] = address_lat
            if address_lng:
                new_fields["address_lng"] = address_lng

            if not new_fields:
                return {}

            updated_profile = await DatabaseRepository.update_by_query(
                Supplier,
                query={"id": self.restaurant_id},
                update_fields=new_fields,
            )
            self._update_from_profile(updated_profile[0])
            return self.get_info()
        except Exception as e:
            get_logger().error(f"Error updating restaurant profile with id {self.restaurant_id}: {str(e)}, update_fields: {update_fields}")
            raise e

    async def delete_restaurant(self) -> bool:
        try:
            await DatabaseRepository.delete_by_query(Supplier, query={"id": self.restaurant_id})
            return True
        except Exception as e:
            get_logger().error(f"Error deleting restaurant account with id {self.restaurant_id}: {str(e)}")
            raise e

    def get_info(self) -> Dict[str, Any]:
        info_dict = dict(
            id=self.restaurant_id,
            owner_user_id=self.owner_user_id,
            name=self.name,
            postal_code=self.postal_code,
            address=self.address,
            address_lat=self.address_lat,
            address_lng=self.address_lng,
            restaurant_licence_id=self.restaurant_licence_id,
        )
        return {key: value for key, value in info_dict.items() if value is not None}

    def _update_from_profile(self, profile: Supplier):
        updated_restaurant = RestaurantDomain._from_profile(profile)
        if not updated_restaurant:
            return
        self.name = updated_restaurant.name
        self.postal_code = updated_restaurant.postal_code
        self.address = updated_restaurant.address
        self.address_lat = updated_restaurant.address_lat
        self.address_lng = updated_restaurant.address_lng
        self.restaurant_licence_id = updated_restaurant.restaurant_licence_id
        self.updated_at = updated_restaurant.updated_at

    @staticmethod
    def _from_profile(profile: Supplier):
        if not profile:
            return None

        return RestaurantDomain(
            restaurant_id=str(profile.id),
            owner_user_id=str(profile.owner_user_id),
            name=profile.name,
            postal_code=profile.postal_code,
            address=profile.address,
            address_lat=profile.address_lat,
            address_lng=profile.address_lng,
            restaurant_licence_id=profile.restaurant_licence_id,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )


    async def load_all_menu_item(self) -> List[MenuDomain]:
        if self.menu is None:
            menu = await DatabaseRepository.fetch_by_query(MenuItem, query={"restaurant_id": self.restaurant_id})
            self.menu = [MenuDomain._from_menu_item(food) for food in menu]
        return self.menu

    async def get_all_menu_item_info(self) -> List[Dict[str, Any]]:
        try:
            if not self.menu:
                await self.load_all_menu_item()

            return [food.get_info() for food in self.menu]
        except Exception as e:
            get_logger().error(f"Error getting addresses info for restaurant with id {self.restaurant_id}: {str(e)}")
            raise e
