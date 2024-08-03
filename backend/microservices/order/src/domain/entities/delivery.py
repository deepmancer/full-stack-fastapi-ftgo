from datetime import datetime
from typing import Optional
from models import DeliveryDetail
from pydantic import BaseModel, ValidationError
from utils.exception import handle_exception
from ftgo_utils.errors import ErrorCodes, BaseError
from ftgo_utils.enums import DeliveryStatus
from domain import get_logger
from domain.entities.base import BaseEntity


class Delivery(BaseEntity):
    document_cls = DeliveryDetail

    def __init__(self, document: DeliveryDetail):
        super().__init__(document)

    @classmethod
    def create(cls, order_id: str, driver_id: Optional[str], source_address_id: str, destination_address_id: str) -> "Delivery":
        delivery_doc: DeliveryDetail = cls.document_cls(
            order_id=order_id,
            driver_id=driver_id,
            delivery_status=DeliveryStatus.PENDING.value,
            source_address_id=source_address_id,
            destination_address_id=destination_address_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return cls(document=delivery_doc)

    @classmethod
    async def load(cls, **kwargs):
        try:
           document: DeliveryDetail = await cls.fetch_document(**kwarg)
           return cls(document=document)
        except Exception as e:
            payload = query
            get_logger().error(ErrorCodes.DELIVERY_NOT_FOUND_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DELIVERY_NOT_FOUND_ERROR, payload=payload)

    async def save(self):
        try:
            await self.document.insert()
        except ValidationError as e:
            payload = {"order_id": self.document.order_id}
            get_logger().error(ErrorCodes.SAVE_DELIVERY_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.SAVE_DELIVERY_ERROR, payload=payload)

    async def update_status(self, status: DeliveryStatus):
        try:
            if status not in DeliveryStatus:
                raise BaseError(error_code=ErrorCodes.INVALID_DELIVERY_STATUS_ERROR, payload={"status": status.value})
            
            self.document.delivery_status = status.value
            await self.document.save()
        except Exception as e:
            payload = {"order_id": self.document.order_id, "status": status.value}
            get_logger().error(ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload=payload)

    async def assign_driver(self, driver_id: str):
        try:
            if self.document.delivery_status != DeliveryStatus.PENDING.value:
                raise BaseError(error_code=ErrorCodes.ASSIGN_DRIVER_ERROR, payload={"status": self.document.delivery_status})
            
            self.document.driver_id = driver_id
            await self.update_status(DeliveryStatus.ASSIGNED)
        except Exception as e:
            payload = {"order_id": self.document.order_id, "driver_id": driver_id}
            get_logger().error(ErrorCodes.ASSIGN_DRIVER_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ASSIGN_DRIVER_ERROR, payload=payload)

    async def mark_as_picked_up(self):
        try:
            if self.document.delivery_status != DeliveryStatus.ASSIGNED.value:
                raise BaseError(error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload={"status": self.document.delivery_status})
            
            await self.update_status(DeliveryStatus.PICKED_UP)
        except Exception as e:
            payload = {"order_id": self.document.order_id}
            get_logger().error(ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload=payload)

    async def mark_as_delivered(self):
        try:
            if self.document.delivery_status != DeliveryStatus.PICKED_UP.value:
                raise BaseError(error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload={"status": self.document.delivery_status})
            
            await self.update_status(DeliveryStatus.DELIVERED)
        except Exception as e:
            payload = {"order_id": self.document.order_id}
            get_logger().error(ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload=payload)

    async def cancel(self):
        try:
            if self.document.delivery_status not in {DeliveryStatus.PENDING.value, DeliveryStatus.ASSIGNED.value}:
                raise BaseError(error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload={"status": self.document.delivery_status})
            
            await self.update_status(DeliveryStatus.CANCELLED)
        except Exception as e:
            payload = {"order_id": self.document.order_id}
            get_logger().error(ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload=payload)
