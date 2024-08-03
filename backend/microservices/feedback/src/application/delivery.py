from typing import Dict, Any, List, Optional
from domain.delivery_rating import DeliveryRatingHandler

class DeliveryRatingService:
    @staticmethod
    async def create_delivery_rating(
        delivery_id: str,
        order_id: str,
        customer_id: str,
        rating: int,
        feedback: Optional[str] = None,
        driver_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        return await DeliveryRatingHandler.create_delivery_rating(
            delivery_id=delivery_id,
            order_id=order_id,
            customer_id=customer_id,
            rating=rating,
            feedback=feedback,
            driver_id=driver_id,
            **kwargs
        )

    @staticmethod
    async def update_delivery_rating(
        delivery_id: str,
        order_id: str,
        customer_id: str,
        rating: int,
        feedback: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        return await DeliveryRatingHandler.update_delivery_rating(
            delivery_id=delivery_id,
            order_id=order_id,
            customer_id=customer_id,
            rating=rating,
            feedback=feedback,
            **kwargs
        )

    @staticmethod
    async def get_delivery_rating(order_id: str, **kwargs) -> Dict[str, Any]:
        return await DeliveryRatingHandler.get_rating(order_id=order_id, **kwargs)

    @staticmethod
    async def get_customer_delivery_ratings(customer_id: str, **kwargs) -> List[Dict[str, Any]]:
        return await DeliveryRatingHandler.get_customer_delivery_ratings(customer_id=customer_id, **kwargs)

    @staticmethod
    async def get_driver_delivery_ratings(driver_id: str, **kwargs) -> List[Dict[str, Any]]:
        return await DeliveryRatingHandler.get_driver_delivery_ratings(driver_id=driver_id, **kwargs)
