from typing import Dict

from services.base import Microservice


class OrderService(Microservice):
    _service_name = 'order'

    @classmethod
    async def get_order_history(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.history', data=data)

    @classmethod
    async def create_order(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.create', data=data)

    @classmethod
    async def update_order(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.update', data=data)

    @classmethod
    async def restaurant_confirm(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.restaurant.confirm', data=data)

    @classmethod
    async def restaurant_reject(cls, data: Dict) -> Dict:
        return await cls._call_rpc('order.restaurant.reject', data=data)