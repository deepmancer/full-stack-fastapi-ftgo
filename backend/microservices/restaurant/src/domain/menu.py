from typing import Optional, Dict, Any
from data_access.repository import DatabaseRepository
from models.menu import MenuItem

import ftgo_utils as utils

class MenuDomain:
    def __init__(
        self,
        item_id: str,
        restaurant_id: str,
        name: str,
        price: float,
        description: str,
        created_at: str,
        updated_at: Optional[str],
    ):
        self.item_id = item_id
        self.restaurant_id = restaurant_id
        self.name = name
        self.price = price
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    async def add_item(
        restaurant_id: str,
        name: str,
        price: float,
        description: str,
    ) -> "MenuDomain":
        item_id = utils.uuid_gen.uuid4()
        new_item = MenuItem(
            item_id=item_id,
            restaurant_id=restaurant_id,
            name=name,
            price=price,
            description=description,
        )
        new_item = await DatabaseRepository.insert(new_item)
        return item_id

    @staticmethod
    async def load(item_id: str) -> "MenuDomain":
        menu_item = await DatabaseRepository.fetch_by_query(MenuItem, query={"item_id": item_id}, one_or_none=True)
        if not menu_item:
            return None
        return MenuDomain._from_menu_item(menu_item)

    @staticmethod
    async def update_item(
        item_id: str,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        update_fields = {}
        if name:
            update_fields["name"] = name
        if price is not None:
            update_fields["price"] = price
        if description:
            update_fields["description"] = description

        updated_item = await DatabaseRepository.update_by_query(
            MenuItem,
            query={"item_id": item_id},
            update_fields=update_fields,
        )
        return MenuDomain._from_menu_item(updated_item[0]).to_dict()

    @staticmethod
    async def delete_item(item_id: str) -> Dict[str, Any]:
        await DatabaseRepository.delete_by_query(MenuItem, query={"item_id": item_id})
        return {"item_id": item_id}

    @staticmethod
    def _from_menu_item(menu_item: MenuItem) -> "MenuDomain":
        return MenuDomain(
            item_id=menu_item.item_id,
            restaurant_id=menu_item.restaurant_id,
            name=menu_item.name,
            price=menu_item.price,
            description=menu_item.description,
            created_at=menu_item.created_at,
            updated_at=menu_item.updated_at,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
