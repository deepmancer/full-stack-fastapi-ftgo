from typing import Any, Dict, List, Optional
from uuid import uuid4

from config.timezone import tz
from utils.time import utcnow
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.order import Order
from data_access.repository.cache_repository import CacheRepository
from data_access.repository.db_repository import DatabaseRepository

from domain.uuid_generator import UUIDGenerator
from domain import get_logger
from domain.exceptions import (
    RestaurantExistsError,
    MenuCreationError,
    MenuItemError,
    OrderError,
    RestaurantNotFoundError,
)


class RestaurantDomain:
    def __init__(
            self,
            restaurant_id: str,
            name: str,
            address: str,
            phone_number: str,
            created_at: str,
            updated_at: Optional[str],
    ):
        self.restaurant_id = restaurant_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.created_at = created_at
        self.updated_at = updated_at

        self.menu_items = None
        self.orders = None

    @staticmethod
    async def load(restaurant_id: str):
        try:
            restaurant_profile = await DatabaseRepository.fetch_by_query(Restaurant, query={"id": restaurant_id},
                                                                         one_or_none=True)
            if not restaurant_profile:
                raise RestaurantNotFoundError(dict(restaurant_id=restaurant_id))

            restaurant = RestaurantDomain._from_profile(restaurant_profile)
            return restaurant
        except Exception as e:
            get_logger().error(str(e), restaurant_id=restaurant_id)
            raise e

    @staticmethod
    async def register(
            name: str,
            address: str,
            phone_number: str,
    ) -> str:
        try:
            current_records = await DatabaseRepository.fetch_by_query(Restaurant, query={"phone_number": phone_number})
            if current_records:
                raise RestaurantExistsError(phone_number=phone_number)

            restaurant_id = UUIDGenerator.generate()

            new_profile = Restaurant(
                id=restaurant_id,
                name=name,
                address=address,
                phone_number=phone_number,
            )
            new_profile = await DatabaseRepository.insert(new_profile)

            restaurant = RestaurantDomain._from_profile(new_profile)

            get_logger().info(
                f"Restaurant with restaurant_id: {restaurant_id} and phone_number: {phone_number} was created successfully")

            return restaurant_id

        except Exception as e:
            get_logger().error(str(e), phone_number=phone_number)
            raise e

    async def update_info(self, name: str, address: str, phone_number: str):
        try:
            updated_fields = {
                "name": name,
                "address": address,
                "phone_number": phone_number,
                "updated_at": utcnow()
            }
            updated_profile = (await DatabaseRepository.update_by_query(
                Restaurant, query={"id": self.restaurant_id}, update_fields=updated_fields
            ))[0]

            self.name = updated_profile.name
            self.address = updated_profile.address
            self.phone_number = updated_profile.phone_number
            self.updated_at = updated_profile.updated_at
        except Exception as e:
            get_logger().error(str(e), restaurant_id=self.restaurant_id)
            raise e

    async def add_menu_item(self, name: str, description: str, price: float) -> str:
        try:
            menu_item_id = UUIDGenerator.generate()
            new_menu_item = MenuItem(
                id=menu_item_id,
                restaurant_id=self.restaurant_id,
                name=name,
                description=description,
                price=price,
            )
            new_menu_item = await DatabaseRepository.insert(new_menu_item)

            if self.menu_items is None:
                self.menu_items = [new_menu_item]
            else:
                self.menu_items.append(new_menu_item)

            return new_menu_item.id
        except Exception as e:
            get_logger().error(str(e), restaurant_id=self.restaurant_id, name=name)
            raise MenuCreationError(restaurant_id=self.restaurant_id) from e

    async def update_menu_item(self, item_id: str, name: Optional[str] = None, description: Optional[str] = None,
                               price: Optional[float] = None):
        try:
            update_fields = {}
            if name:
                update_fields["name"] = name
            if description:
                update_fields["description"] = description
            if price:
                update_fields["price"] = price

            update_fields["updated_at"] = utcnow()

            updated_menu_item = (await DatabaseRepository.update_by_query(
                MenuItem, query={"id": item_id, "restaurant_id": self.restaurant_id}, update_fields=update_fields
            ))[0]

            if self.menu_items:
                for item in self.menu_items:
                    if item.id == item_id:
                        item.name = updated_menu_item.name
                        item.description = updated_menu_item.description
                        item.price = updated_menu_item.price
                        item.updated_at = updated_menu_item.updated_at
                        break
        except Exception as e:
            get_logger().error(str(e), restaurant_id=self.restaurant_id, item_id=item_id)
            raise MenuItemError(restaurant_id=self.restaurant_id, item_id=item_id) from e

    async def delete_menu_item(self, item_id: str):
        try:
            await DatabaseRepository.delete_by_query(MenuItem,
                                                     query={"id": item_id, "restaurant_id": self.restaurant_id})
            if self.menu_items:
                self.menu_items = [item for item in self.menu_items if item.id != item_id]
        except Exception as e:
            get_logger().error(str(e), restaurant_id=self.restaurant_id, item_id=item_id)
            raise MenuItemError(restaurant_id=self.restaurant_id, item_id=item_id) from e

    async def receive_order(self, customer_id: str, items: List[Dict[str, Any]],
                            special_instructions: Optional[str] = None) -> str:
        try:
            order_id = UUIDGenerator.generate()
            new_order = Order(
                id=order_id,
                restaurant_id=self.restaurant_id,
                customer_id=customer_id,
                items=items,
                special_instructions=special_instructions,
            )
            new_order = await DatabaseRepository.insert(new_order)

            if self.orders is None:
                self.orders = [new_order]
            else:
                self.orders.append(new_order)

            return new_order.id
        except Exception as e:
            get_logger().error(str(e), restaurant_id=self.restaurant_id, customer_id=customer_id)
            raise OrderError(restaurant_id=self.restaurant_id) from e

    async def get_orders(self) -> List[Dict[str, Any]]:
        try:
            if not self.orders:
                await self.load_orders()

            return [order.get_info() for order in self.orders]
        except Exception as e:
            get_logger().error(str(e), restaurant_id=self.restaurant_id)
            raise OrderError(restaurant_id=self.restaurant_id) from e

    def to_dict(self) -> Dict[str, Any]:
        return {
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    async def load_orders(self) -> List[Order]:
        if self.orders is None:
            orders = await DatabaseRepository.fetch_by_query(Order, query={"restaurant_id": self.restaurant_id})
            self.orders = [Order._from_order(order) for order in orders]
        return self.orders

    def _get_secret(self) -> str:
        return f"{self.phone_number}{self.name}"

    @staticmethod
    def _from_profile(profile: Restaurant):
        if not profile:
            return None

        return RestaurantDomain(
            restaurant_id=str(profile.id),
            name=profile.name,
            address=profile.address,
            phone_number=profile.phone_number,
            created_at=profile.created_at.astimezone(tz) if profile.created_at else None,
            updated_at=profile.updated_at.astimezone(tz) if profile.updated_at else None,
        )
