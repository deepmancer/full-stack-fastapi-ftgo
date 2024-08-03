from datetime import datetime
from typing import List, Optional
from models.order_item import OrderItem as OrderItemDocument
from models.order_status import OrderStatus as OrderStatusDocument
from models.order import Order as OrderDocument
from pydantic import BaseModel, ValidationError
from utils.exception import handle_exception
from ftgo_utils.errors import ErrorCodes, BaseError
from ftgo_utils.enums import OrderStatus, PaymentStatus
from domain import get_logger
from domain.entities.base import BaseEntity


class Order(BaseEntity):
    document_cls = OrderDocument

    def __init__(self, document: OrderDocument):
        super().__init__(document)

    @classmethod
    def create(cls, customer_id: str, restaurant_id: str, special_instructions: Optional[str] = None) -> "Order":
        order_doc = OrderDocument(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            total_amount=0,
            order_items=[],
            status_history=[],
            special_instructions=special_instructions,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return cls(document=order_doc)

    @classmethod
    async def load(cls, **kwargs):
        try:
            document: OrderDocument = await cls.fetch_document(**kwargs)
            return cls(document=document)
        except Exception as e:
            payload = "query"
            get_logger().error(ErrorCodes.ORDER_NOT_FOUND_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ORDER_NOT_FOUND_ERROR, payload=payload)

    async def save(self):
        try:
            await self.document.insert()
        except ValidationError as e:
            payload = {"customer_id": self.document.customer_id}
            get_logger().error(ErrorCodes.SAVE_ORDER_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.SAVE_ORDER_ERROR, payload=payload)

    async def add_order_item(self, order_item: OrderItemDocument):
        try:
            self.document.order_items.append(order_item)
            await self.calculate_total()
        except Exception as e:
            payload = {"order_id": str(self.document.id), "order_item": str(order_item.menu_item_id)}
            get_logger().error(ErrorCodes.ADD_ORDER_ITEM_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ADD_ORDER_ITEM_ERROR, payload=payload)

    async def remove_order_item(self, menu_item_id: str):
        try:
            self.document.order_items = [item for item in self.document.order_items if item.menu_item_id != menu_item_id]
            await self.calculate_total()
        except Exception as e:
            payload = {"order_id": str(self.document.id), "menu_item_id": menu_item_id}
            get_logger().error(ErrorCodes.REMOVE_ORDER_ITEM_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.REMOVE_ORDER_ITEM_ERROR, payload=payload)

    async def calculate_total(self):
        try:
            self.document.total_amount = sum(item.subtotal for item in self.document.order_items)
            await self.document.save()
        except Exception as e:
            payload = {"order_id": str(self.document.id)}
            get_logger().error(ErrorCodes.CALCULATE_TOTAL_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CALCULATE_TOTAL_ERROR, payload=payload)

    async def change_status(self, status: OrderStatus, changed_by: Optional[str] = None, comments: Optional[str] = None):
        try:
            if status == OrderStatus.CANCELLED and self.document.status == OrderStatus.DELIVERED.value:
                raise BaseError(error_code=ErrorCodes.CHANGE_ORDER_STATUS_ERROR, payload={"status": self.document.status})
            
            new_status = OrderStatusDocument(
                order_id=str(self.document.id),
                status=status.value,
                changed_by=changed_by,
                comments=comments,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.document.status_history.append(new_status)
            self.document.status = new_status
            await self.document.save()
        except Exception as e:
            payload = {"order_id": str(self.document.id), "status": status.value}
            get_logger().error(ErrorCodes.CHANGE_ORDER_STATUS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CHANGE_ORDER_STATUS_ERROR, payload=payload)

    async def process_payment(self, payment_id: str):
        try:
            self.document.payment_id = payment_id
            await self.change_status(OrderStatus.OUT_FOR_DELIVERY)
            await self.save()
        except Exception as e:
            payload = {"order_id": str(self.document.id), "payment_id": payment_id}
            get_logger().error(ErrorCodes.PROCESS_PAYMENT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.PROCESS_PAYMENT_ERROR, payload=payload)

    async def mark_ready_for_pickup(self):
        try:
            await self.change_status(OrderStatus.READY_FOR_PICKUP)
            await self.save()
        except Exception as e:
            payload = {"order_id": str(self.document.id)}
            get_logger().error(ErrorCodes.MARK_READY_FOR_PICKUP_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.MARK_READY_FOR_PICKUP_ERROR, payload=payload)

    async def cancel_order(self):
        try:
            await self.change_status(OrderStatus.CANCELLED)
            await self.save()
        except Exception as e:
            payload = {"order_id": str(self.document.id)}
            get_logger().error(ErrorCodes.CANCEL_ORDER_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CANCEL_ORDER_ERROR, payload=payload)
