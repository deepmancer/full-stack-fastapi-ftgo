from typing import Dict, Optional, Any
from ftgo_utils.enums import OrderStatus as OrderStatusEnum
from domain.entities import Order

class RestaurantHandler:
    @staticmethod
    async def confirm_order(order_id: str, **kwargs) -> Dict[str, Any]:
        order = await RestaurantHandler.load_entity(Order, order_id)
        await order.change_status(OrderStatusEnum.CONFIRMED)
        await RestaurantHandler.save_entity(order)
        return order.document.dict()

    @staticmethod
    async def reject_order(order_id: str, reason: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        order = await RestaurantHandler.load_entity(Order, order_id)
        await order.change_status(OrderStatusEnum.REJECTED, comments=reason)
        await RestaurantHandler.save_entity(order)
        return order.document.dict()
