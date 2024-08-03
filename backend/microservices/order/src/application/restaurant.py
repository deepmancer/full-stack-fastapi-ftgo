from typing import Dict, Optional, Any
from ftgo_utils.enums import OrderStatus as OrderStatusEnum
from domain.restaurant import RestaurantHandler

class RestaurantService:
    @staticmethod
    async def confirm_order(order_id: str, **kwargs) -> Dict[str, Any]:
        return await RestaurantHandler.confirm_order(order_id, **kwargs)

    @staticmethod
    async def reject_order(order_id: str, reason: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        return await RestaurantHandler.reject_order(order_id, reason, **kwargs)
