from datetime import datetime
from typing import Optional
from models.order_item import OrderItem as OrderItemDocument
from pydantic import BaseModel, ValidationError
from utils.exception import handle_exception
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger
from domain.entities.base import BaseEntity


class OrderItem(BaseEntity):
    document_cls = OrderItemDocument
    
    def __init__(self, document: OrderItemDocument):
        super().__init__(document)

    @classmethod
    def create(cls, order_id: str, menu_item_id: str, quantity: int, item_price: float, special_instructions: Optional[str] = None) -> "OrderItem":
        order_item_doc = OrderItemDocument(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            item_price=item_price,
            subtotal=quantity * item_price,
            special_instructions=special_instructions,
            created_at=datetime.utcnow(),
        )
        return cls(document=order_item_doc)

    @classmethod
    async def load(cls, **kwargs):
        try:
            document: OrderItemDocument = await cls.fetch_document(**kwargs)
            return cls(document=document)
        except Exception as e:
            payload = query
            get_logger().error(ErrorCodes.ORDER_NOT_FOUND_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ORDER_NOT_FOUND_ERROR, payload=payload)

    async def save(self):
        try:
            await self.document.insert()
        except ValidationError as e:
            payload = {"order_id": self.document.order_id, "menu_item_id": self.document.menu_item_id}
            get_logger().error(ErrorCodes.SAVE_ORDER_ITEM_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.SAVE_ORDER_ITEM_ERROR, payload=payload)

    async def update_quantity(self, quantity: int):
        try:
            self.document.quantity = quantity
            self.document.subtotal = self.document.quantity * self.document.item_price
            await self.document.save()
        except Exception as e:
            payload = {"order_id": self.document.order_id, "quantity": quantity}
            get_logger().error(ErrorCodes.UPDATE_ORDER_ITEM_QUANTITY_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_ORDER_ITEM_QUANTITY_ERROR, payload=payload)

    async def update_item_price(self, new_price: float):
        try:
            self.document.item_price = new_price
            self.document.subtotal = self.document.quantity * self.document.item_price
            await self.document.save()
        except Exception as e:
            payload = {"order_id": self.document.order_id, "new_price": new_price}
            get_logger().error(ErrorCodes.UPDATE_ORDER_ITEM_PRICE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_ORDER_ITEM_PRICE_ERROR, payload=payload)
