import pymongo

from datetime import datetime
from typing import Optional, List
from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel
from models.order_item import OrderItem
from models.order_status import OrderStatus

class Order(Document):
    customer_id: str
    restaurant_id: str
    total_amount: float = Field(..., gt=0)
    status: OrderStatus
    order_items: List[Link[OrderItem]] = []
    status_history: Optional[List[Link[OrderStatus]]] = [] 
    payment_id: Optional[str] = None
    special_instructions: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "orders"
        indexes = [
            IndexModel([("customer_id", pymongo.ASCENDING)], name="order_customer_id_index"),
            IndexModel([("restaurant_id", pymongo.ASCENDING)], name="order_restaurant_id_index"),
            IndexModel([("created_at", pymongo.DESCENDING)], name="order_created_at_index"),
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
