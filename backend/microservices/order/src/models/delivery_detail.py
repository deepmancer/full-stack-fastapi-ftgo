import pymongo

from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field
from pymongo import IndexModel



class DeliveryDetail(Document):
    order_id: str
    driver_id: str
    delivery_status: str = Field(..., max_length=50)
    source_address_id: str
    destination_address_id: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "delivery_details"
        indexes = [
            IndexModel([("delivery_status", pymongo.ASCENDING)], name="delivery_detail_delivery_status_index"),
            IndexModel([("order_id", pymongo.ASCENDING)], name="delivery_detail_order_id_index"),
            IndexModel([("driver_id", pymongo.ASCENDING)], name="delivery_detail_driver_id_index"),
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
