from typing import Dict, Any, List, Optional
from domain.order import OrderHandler

class OrderService:
    @staticmethod
    async def create_order(
        customer_id: str,
        restaurant_id: str,
        order_items_data: List[Dict[str, Any]],
        special_instructions: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        return await OrderHandler.create_order(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            order_items_data=order_items_data,
            special_instructions=special_instructions,
            **kwargs
        )

    @staticmethod
    async def update_order(order_id: str, updated_items_data: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        return await OrderHandler.update_order(order_id, updated_items_data, **kwargs)

    @staticmethod
    async def get_order_details(order_id: str, **kwargs) -> Dict[str, Any]:
        return await OrderHandler.get_order_details(order_id, **kwargs)
