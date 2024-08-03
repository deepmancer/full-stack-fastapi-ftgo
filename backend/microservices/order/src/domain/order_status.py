from typing import Optional, Any
from domain.entities import OrderStatus, Order
from ftgo_utils.enums import OrderStatus as OrderStatusEnum
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger

class OrderStatusHandler:
    @staticmethod
    async def change_order_status(
        order_id: str,
        new_status: OrderStatusEnum,
        changed_by: Optional[str] = None,
        comments: Optional[str] = None,
    ):
        try:
            order = await Order.load(order_id)
            if not order:
                raise BaseError(error_code=ErrorCodes.ORDER_NOT_FOUND_ERROR, payload={"order_id": order_id})
            
            await order.change_status(new_status, changed_by=changed_by, comments=comments)
            await order.save()
        except Exception as e:
            payload = {"order_id": order_id, "new_status": new_status.value}
            get_logger().error(ErrorCodes.CHANGE_ORDER_STATUS_ERROR.value, payload=payload)
            await handle_exception(e, error_code=ErrorCodes.CHANGE_ORDER_STATUS_ERROR, payload=payload)

    @staticmethod
    async def cancel_order(order_id: str):
        await OrderStatusHandler.change_order_status(order_id, OrderStatusEnum.CANCELLED)

    @staticmethod
    async def mark_order_ready_for_pickup(order_id: str):
        await OrderStatusHandler.change_order_status(order_id, OrderStatusEnum.READY_FOR_PICKUP)

    @staticmethod
    async def process_payment_confirmation(order_id: str):
        try:
            order = await Order.load(order_id)
            if not order:
                raise BaseError(error_code=ErrorCodes.ORDER_NOT_FOUND_ERROR, payload={"order_id": order_id})
            
            await order.process_payment(order.payment_id)
            await OrderStatusHandler.change_order_status(order_id, OrderStatusEnum.PAID)
        except Exception as e:
            payload = {"order_id": order_id}
            get_logger().error(ErrorCodes.PROCESS_PAYMENT_ERROR.value, payload=payload)
            await handle_exception(e, error_code=ErrorCodes.PROCESS_PAYMENT_ERROR, payload=payload)
