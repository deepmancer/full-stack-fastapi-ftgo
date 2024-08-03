from typing import Dict, Any, List, Optional
from domain.order_rating import OrderRatingHandler

class OrderRatingService:
    @staticmethod
    async def create_order_rating(
        order_id: str,
        customer_id: str,
        rating: int,
        feedback: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        return await OrderRatingHandler.create_order_rating(
            order_id=order_id,
            customer_id=customer_id,
            rating=rating,
            feedback=feedback,
            **kwargs
        )

    @staticmethod
    async def update_order_rating(
        order_id: str,
        customer_id: str,
        rating: int,
        feedback: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        return await OrderRatingHandler.update_order_rating(
            order_id=order_id,
            customer_id=customer_id,
            rating=rating,
            feedback=feedback,
            **kwargs
        )

    @staticmethod
    async def get_order_rating(order_id: str, **kwargs) -> Dict[str, Any]:
        return await OrderRatingHandler.get_rating(order_id=order_id, **kwargs)

    @staticmethod
    async def get_customer_order_ratings(customer_id: str, **kwargs) -> List[Dict[str, Any]]:
        return await OrderRatingHandler.get_customer_order_ratings(customer_id=customer_id, **kwargs)

    @staticmethod
    async def get_restaurant_order_ratings(restaurant_id: str, **kwargs) -> List[Dict[str, Any]]:
        return await OrderRatingHandler.get_restaurant_order_ratings(restaurant_id=restaurant_id, **kwargs)
