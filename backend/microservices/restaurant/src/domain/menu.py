from typing import Optional, Dict, Any
from ftgo_utils.errors import BaseError, ErrorCodes

from domain import get_logger
from data_access.repository import DatabaseRepository
from models.menu import MenuItem
from utils import handle_exception

import ftgo_utils as utils

class MenuDomain:
    def __init__(
        self,
        item_id: str,
        restaurant_id: str,
        name: str,
        price: float,
        count: int,
        description: str,
        created_at: str,
        updated_at: Optional[str],
    ):
        self.item_id = item_id
        self.restaurant_id = restaurant_id
        self.name = name
        self.price = price
        self.count = count
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    async def add_item(
        restaurant_id: str,
        name: str,
        price: float,
        count: int,
        description: str,
    ) -> "MenuDomain":
        try:
            item_id = utils.uuid_gen.uuid4()
            new_item = MenuItem(
                item_id=item_id,
                restaurant_id=restaurant_id,
                name=name,
                price=price,
                count=count,
                description=description,
            )
            new_item = await DatabaseRepository.insert(new_item)
            return item_id
        except Exception as e:
            payload = {
                "restaurant_id": restaurant_id,
                "name": name,
                "price": price,
                "count": count,
                "description": description,
            }
            #TODO change error code
            get_logger().error(ErrorCodes.ADD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ADD_ADDRESS_ERROR, payload=payload)

    @staticmethod
    async def load(item_id: str) -> Optional["MenuDomain"]:
        try:
            menu_item = await DatabaseRepository.fetch_by_query(MenuItem, query={"item_id": item_id}, one_or_none=True)
            if not menu_item:
                return None
            return MenuDomain._from_schema(menu_item)
        except Exception as e:
            payload = {"item_id": item_id}
            #TODO change error code
            get_logger().error(ErrorCodes.LOAD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.LOAD_ADDRESS_ERROR, payload=payload)

    @staticmethod
    async def update_item(
        item_id: str,
        name: Optional[str] = None,
        price: Optional[float] = None,
        count: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        update_fields = {}
        if name:
            update_fields["name"] = name
        if price is not None:
            update_fields["price"] = price
        if description:
            update_fields["description"] = description
        if count:
            update_fields["count"] = count
        try:
            updated_item = await DatabaseRepository.update_by_query(
                MenuItem,
                query={"item_id": item_id},
                update_fields=update_fields,
            )
            return MenuDomain._from_schema(updated_item[0]).to_dict()
        except Exception as e:
            payload = {
                "user_id": item_id,
                "update_fields": update_fields,
            }
            #TODO change error code
            get_logger().error(ErrorCodes.UPDATE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_ADDRESS_ERROR, payload=payload)

    @staticmethod
    async def delete_item(item_id: str) -> Dict[str, Any]:
        try:
            await DatabaseRepository.delete_by_query(MenuItem, query={"item_id": item_id})
            return {"item_id": item_id}
        except Exception as e:
            payload = {"item_id": item_id}
            #TODO change error code
            get_logger().error(ErrorCodes.DELETE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DELETE_ADDRESS_ERROR, payload=payload)

    @staticmethod
    def _from_schema(menu_item: MenuItem) -> "MenuDomain":
        return MenuDomain(
            item_id=menu_item.item_id,
            restaurant_id=menu_item.restaurant_id,
            name=menu_item.name,
            price=menu_item.price,
            count=menu_item.count,
            description=menu_item.description,
            created_at=str(menu_item.created_at),
            updated_at=str(menu_item.updated_at),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "price": self.price,
            "count": self.count,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
