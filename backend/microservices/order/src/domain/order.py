from typing import List, Optional, Any
from domain.entities import Order, OrderItem
from domain.order_status import OrderStatusHandler
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger
from utils import handle_exception

class OrderHandler:
    @staticmethod
    async def create_order(
        customer_id: str,
        restaurant_id: str,
        order_items: List[OrderItem],
        special_instructions: Optional[str] = None,
    ) -> Order:
        try:
            order = Order.create(
                customer_id=customer_id,
                restaurant_id=restaurant_id,
                special_instructions=special_instructions
            )
            for item in order_items:
                await order.add_order_item(item)
            
            await order.save()
            return order
        except Exception as e:
            payload = {"customer_id": customer_id, "restaurant_id": restaurant_id}
            get_logger().error(ErrorCodes.CREATE_ORDER_ERROR.value, payload=payload)
            await handle_exception(e, error_code=ErrorCodes.CREATE_ORDER_ERROR, payload=payload)

    @staticmethod
    async def update_order(order_id: str, updated_items: List[OrderItem]):
        try:
            order = await Order.load(order_id)
            if not order:
                raise BaseError(error_code=ErrorCodes.ORDER_NOT_FOUND_ERROR, payload={"order_id": order_id})
            
            await order.update_order_items(updated_items)
            await order.save()
        except Exception as e:
            payload = {"order_id": order_id}
            get_logger().error(ErrorCodes.UPDATE_ORDER_ERROR.value, payload=payload)
            await handle_exception(e, error_code=ErrorCodes.UPDATE_ORDER_ERROR, payload=payload)

    @staticmethod
    async def get_order_details(order_id: str) -> Order:
        order = await Order.load(order_id)
        if not order:
            raise BaseError(error_code=ErrorCodes.ORDER_NOT_FOUND_ERROR, payload={"order_id": order_id})
        return order
