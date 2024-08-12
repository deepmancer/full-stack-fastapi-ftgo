from typing import Dict

from services.base import Microservice


class RestaurantService(Microservice):
    _service_name = 'restaurant'

    @classmethod
    async def register(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.supplier.register', data=data)

    @classmethod
    async def get_restaurant_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.supplier.get_restaurant_info', data=data)

    @classmethod
    async def get_all_restaurant_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.supplier.get_all_restaurant_info', data=data)

    @classmethod
    async def get_supplier_restaurant_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.supplier.get_supplier_restaurant_info', data=data)

    @classmethod
    async def update_information(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.supplier.update_information', data=data)

    @classmethod
    async def delete_restaurant(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.supplier.delete_restaurant', data=data)

