from typing import Dict

from services.base import Microservice


class FeedbackService(Microservice):
    _service_name = 'feedback'

    # Delivery Rating Methods
    @classmethod
    async def create_delivery_rating(cls, data: Dict) -> Dict:
        return await cls._call_rpc('delivery.rating.create', data=data)

    @classmethod
    async def update_delivery_rating(cls, data: Dict) -> Dict:
        return await cls._call_rpc('delivery.rating.update', data=data)

    @classmethod
    async def get_delivery_rating(cls, data: Dict) -> Dict:
        return await cls._call_rpc('delivery.rating.get', data=data)

    @classmethod
    async def get_customer_delivery_ratings(cls, data: Dict) -> Dict:
        return await cls._call_rpc('delivery.rating.get_customer_ratings', data=data)

    @classmethod
    async def get_driver_delivery_ratings(cls, data: Dict) -> Dict:
        return await cls._call_rpc('delivery.rating.get_driver_ratings', data=data)

    # Order Rating Methods
    @classmethod
    async def create_order_rating(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.rating.create', data=data)

    @classmethod
    async def update_order_rating(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.rating.update', data=data)

    @classmethod
    async def get_order_rating(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.rating.get', data=data)

    @classmethod
    async def get_customer_order_ratings(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.rating.get_customer_ratings', data=data)

    @classmethod
    async def get_restaurant_order_ratings(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.rating.get_restaurant_ratings', data=data)
