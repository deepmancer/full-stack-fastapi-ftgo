from datetime import datetime
from typing import Optional
from models.order_status import OrderStatus as OrderStatusDocument
from pydantic import BaseModel, ValidationError
from utils.exception import handle_exception
from ftgo_utils.errors import ErrorCodes, BaseError
from ftgo_utils.enums import OrderStatus
from domain.entities.base import BaseEntity
from domain import get_logger

class OrderStatus(BaseEntity):
    document_cls = OrderStatusDocument
    
    def __init__(self, document: OrderStatusDocument):
        super().__init__(document)

    @classmethod
    def create(cls, order_id: str, status: OrderStatus, changed_by: Optional[str] = None, comments: Optional[str] = None) -> "OrderStatus":
        order_status_doc = OrderStatusDocument(
            order_id=order_id,
            status=status.value,
            changed_by=changed_by,
            comments=comments,
            created_at=datetime.utcnow(),
        )
        return cls(document=order_status_doc)

    @classmethod
    async def load(cls, **kwargs):
        try:
            document: OrderStatusDocument = await cls.fetch_document(**kwargs)
            return cls(document=document)
        except Exception as e:
            payload = query
            get_logger().error(ErrorCodes.ORDER_NOT_FOUND_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ORDER_NOT_FOUND_ERROR, payload=payload)

    async def save(self):
        try:
            await self.document.insert()
        except ValidationError as e:
            payload = {"order_id": self.document.order_id, "status": self.document.status}
            get_logger().error(ErrorCodes.SAVE_ORDER_STATUS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.SAVE_ORDER_STATUS_ERROR, payload=payload)
