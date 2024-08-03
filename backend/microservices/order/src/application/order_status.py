from typing import Dict, Optional, Any
from ftgo_utils.enums import OrderStatus as OrderStatusEnum
from domain.order_status import OrderStatusHandler

class OrderStatusService:
    @staticmethod
    async def change_order_status(order_id: str, new_status: OrderStatusEnum, changed_by: Optional[str] = None, comments: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        return await OrderStatusHandler.change_order_status(
            order_id=order_id,
            new_status=new_status,
            changed_by=changed_by,
            comments=comments,
            **kwargs
        )

    @staticmethod
    async def cancel_order(order_id: str, **kwargs) -> Dict[str, Any]:
        return await OrderStatusHandler.cancel_order(order_id, **kwargs)

    @staticmethod
    async def mark_order_ready_for_pickup(order_id: str, **kwargs) -> Dict[str, Any]:
        return await OrderStatusHandler.mark_order_ready_for_pickup(order_id, **kwargs)
