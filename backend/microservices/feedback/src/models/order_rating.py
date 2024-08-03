import pymongo

from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field
from pymongo import IndexModel

class OrderRating(Document):
    order_id: str = Field(..., index=True)
    customer_id: str = Field(..., index=True)
    rating: int = Field(..., ge=1, le=5)  # Rating from 1 to 5
    feedback: Optional[str] = Field(None, max_length=1000)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "order_ratings"
        indexes = [
            IndexModel([("order_id", pymongo.ASCENDING)], name="order_rating_order_id_index"),
            IndexModel([("customer_id", pymongo.ASCENDING)], name="order_rating_customer_id_index"),
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
