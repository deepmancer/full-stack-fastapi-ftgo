import pymongo

from datetime import datetime
from typing import Optional
from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

class OrderStatus(Document):
    order_id: str
    status: str = Field(..., max_length=50)
    changed_by: Optional[str] = None
    comments: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "order_status"
        indexes = [
            IndexModel([("order_id", pymongo.ASCENDING)], name="order_status_order_id_index"),
            IndexModel([("status", pymongo.ASCENDING)], name="order_status_status_index"),
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
