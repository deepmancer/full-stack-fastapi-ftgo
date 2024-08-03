import pymongo

from datetime import datetime
from typing import Optional
from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

class OrderItem(Document):
    order_id: str
    menu_item_id: str
    quantity: int = Field(..., gt=0)
    item_price: float = Field(..., gt=0)
    subtotal: float = Field(..., gt=0)
    special_instructions: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "order_items"
        indexes = [
            IndexModel([("order_id", pymongo.ASCENDING)], name="order_item_order_id_index"),
            IndexModel([("menu_item_id", pymongo.ASCENDING)], name="order_item_menu_item_id_index"),
        ]
        use_state_management = True
        validate_on_save = True

    @classmethod
    async def before_insert(cls, instance):
        instance.created_at = datetime.utcnow()
        instance.updated_at = datetime.utcnow()

    @classmethod
    async def before_replace(cls, instance):
        instance.updated_at = datetime.utcnow()
