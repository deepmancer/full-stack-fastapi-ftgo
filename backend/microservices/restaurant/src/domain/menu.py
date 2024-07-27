from typing import Optional, Dict, Any
from data_access.repository import DatabaseRepository
from models.menu import MenuItem

import ftgo_utils as utils

class MenuDomain:
    def __init__(
        self,
        item_id: str,
        name: str,
        price: float,
        description: str,
        created_at: str,
        updated_at: Optional[str],
        score: Optional[float],
    ):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.score = score

    @staticmethod
    async def add_item(
        restaurant_id: str,
        name: str,
        price: float,
        description: str,
        score: float = 5.0,
    ) -> "MenuDomain":
        food_id = utils.uuid_gen.uuid4()
        new_item = MenuItem(
            id=food_id,
            restaurant_id=restaurant_id,
            name=name,
            price=price,
            description=description,
            score=score,
        )
        new_item = await DatabaseRepository.insert(new_item)
        return food_id

    @staticmethod
    async def load(item_id: str) -> "MenuDomain":
        menu_item = await DatabaseRepository.fetch_by_query(MenuItem, query={"id": item_id}, one_or_none=True)
        if not menu_item:
            return None
        return MenuDomain._from_menu_item(menu_item)

    @staticmethod
    async def update_item(
        item_id: str,
        name: Optional[str] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
        score: Optional[float] = None,
    ) -> Dict[str, Any]:
        update_fields = {}
        if name:
            update_fields["name"] = name
        if price is not None:
            update_fields["price"] = price
        if description:
            update_fields["description"] = description
        if score is not None:
            update_fields["score"] = score

        updated_item = await DatabaseRepository.update_by_query(
            MenuItem,
            query={"id": item_id},
            update_fields=update_fields,
        )
        return MenuDomain._from_menu_item(updated_item[0]).to_dict()

    @staticmethod
    async def delete_item(item_id: str) -> bool:
        await DatabaseRepository.delete_by_query(MenuItem, query={"id": item_id})
        return True

    @staticmethod
    def _from_menu_item(menu_item: MenuItem) -> "MenuDomain":
        return MenuDomain(
            item_id=str(menu_item.id),
            name=menu_item.name,
            price=menu_item.price,
            description=menu_item.description,
            score=menu_item.score,
            created_at=menu_item.created_at,
            updated_at=menu_item.updated_at,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "score": self.score,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
