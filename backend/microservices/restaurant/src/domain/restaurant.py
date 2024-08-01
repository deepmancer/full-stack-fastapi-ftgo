import asyncio
from typing import Any, Dict, Optional, List

from ftgo_utils.errors import ErrorCodes, BaseError
import ftgo_utils as utils

from data_access.repository import DatabaseRepository
from domain import get_logger
from models.supplier import Supplier
from domain.menu import MenuDomain
from models.menu import MenuItem
from utils import handle_exception


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

    @staticmethod
    async def load(
        owner_user_id: Optional[str] = None,
        restaurant_id: Optional[str] = None,
        raise_error_on_missing: bool = True,
    ) -> Optional["RestaurantDomain"]:
        query_dict = {}
        if restaurant_id:
            query_dict["id"] = restaurant_id
        if owner_user_id:
            query_dict["owner_user_id"] = owner_user_id
        try:
            restaurant_profile = await DatabaseRepository.fetch_by_query(Supplier, query=query_dict, one_or_none=True)
            if not restaurant_profile:
                if raise_error_on_missing:
                    #TODO change error code
                    raise BaseError(error_code=ErrorCodes.USER_NOT_FOUND_ERROR, payload=query_dict)
                return None
            return RestaurantDomain._from_schema(restaurant_profile)
        except Exception as e:
            payload = dict(query=query_dict)
            #TODO change error code
            get_logger().error(ErrorCodes.USER_LOAD_ACCOUNT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOAD_ACCOUNT_ERROR, payload=payload)

    @staticmethod
    async def load_all() -> List["RestaurantDomain"]:
        try:
            all_restaurants = await DatabaseRepository.fetch_by_query(Supplier, query={})
            return [RestaurantDomain._from_schema(restaurant) for restaurant in all_restaurants]
        except Exception as e:
            payload = {}
            # TODO change error code
            get_logger().error(ErrorCodes.USER_LOAD_ACCOUNT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOAD_ACCOUNT_ERROR, payload=payload)

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
                #TODO change error code
                raise BaseError(error_code=ErrorCodes.ACCOUNT_EXISTS_ERROR, payload=dict(owner_user_id=owner_user_id))

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
            get_logger().info(f"Restaurant with user_id: {owner_user_id} and name: {name} was created successfully")

            return restaurant_id
        except Exception as e:
            payload = dict(owner_user_id=owner_user_id, name=name)
            #TODO change error code
            get_logger().error(ErrorCodes.USER_REGISTRATION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_REGISTRATION_ERROR, payload=payload)

    @staticmethod
    async def update_profile_information(
            restaurant_id: str,
            name: Optional[str] = None,
            postal_code: Optional[str] = None,
            address: Optional[str] = None,
            address_lat: Optional[float] = None,
            address_lng: Optional[float] = None,
    ):
        update_fields = {}
        if name:
            update_fields["name"] = name
        if postal_code:
            update_fields["postal_code"] = postal_code
        if address:
            update_fields["address"] = address
        if address_lat:
            update_fields["address_lat"] = address_lat
        if address_lng:
            update_fields["address_lng"] = address_lng

        if not update_fields:
            return restaurant_id
        try:
            updated_item = await DatabaseRepository.update_by_query(
                Supplier,
                query={"id": restaurant_id},
                update_fields=update_fields,
            )
            return RestaurantDomain._from_schema(updated_item[0]).to_dict()
        except Exception as e:
            payload = dict(restaurant_id=restaurant_id, update_fields=update_fields)
            #TODO change error code
            get_logger().error(ErrorCodes.USER_PROFILE_UPDATE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_PROFILE_UPDATE_ERROR, payload=payload)

    async def delete_restaurant(self) -> bool:
        try:
            await DatabaseRepository.delete_by_query(Supplier, query={"id": self.restaurant_id})
            return True
        except Exception as e:
            payload = dict(restaurant_id=self.restaurant_id)
            #TODO change error code
            get_logger().error(ErrorCodes.USER_DELETE_ACCOUNT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_DELETE_ACCOUNT_ERROR, payload=payload)

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

    def _update_from_schema(self, profile: Supplier):
        updated_restaurant = RestaurantDomain._from_schema(profile)
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
    def _from_schema(profile: Supplier):
        return RestaurantDomain(
            restaurant_id=profile.id,
            owner_user_id=profile.owner_user_id,
            name=profile.name,
            postal_code=profile.postal_code,
            address=profile.address,
            address_lat=profile.address_lat,
            address_lng=profile.address_lng,
            restaurant_licence_id=profile.restaurant_licence_id,
            created_at=str(profile.created_at),
            updated_at=str(profile.updated_at),
        )


    async def load_all_menu_item(self):
        try:
            if self.menu is None:
                menu = await DatabaseRepository.fetch_by_query(MenuItem, query={"restaurant_id": self.restaurant_id})
                self.menu = [MenuDomain._from_schema(menu_item) for menu_item in menu]
            return self.menu
        except Exception as e:
            payload = {"restaurant_id": self.restaurant_id}
            #TODO change error code
            get_logger().error(ErrorCodes.BATCH_LOAD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.BATCH_LOAD_ADDRESS_ERROR, payload=payload)

    async def get_all_menu_item_info(self) -> List[Dict[str, Any]]:
        try:
            if not self.menu:
                await self.load_all_menu_item()
            return [food.to_dict() for food in self.menu]
        except Exception as e:
            payload = {"restaurant_id": self.restaurant_id}
            #TODO change error code
            get_logger().error(ErrorCodes.GET_ADDRESSES_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.GET_ADDRESSES_ERROR, payload=payload)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "restaurant_id": self.restaurant_id,
            "owner_user_id": self.owner_user_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "address": self.address,
            "address_lat": self.address_lat,
            "address_lng": self.address_lng,
            "restaurant_licence_id": self.restaurant_licence_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
