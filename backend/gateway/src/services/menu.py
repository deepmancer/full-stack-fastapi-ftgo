from typing import Dict

from services.base import Microservice


class MenuService(Microservice):
    _service_name = 'menu'

    @classmethod
    async def add_item(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.menu.add_item', data=data)

    @classmethod
    async def get_item_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.menu.get_item_info', data=data)

    @classmethod
    async def update_item(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.menu.update_item', data=data)

    @classmethod
    async def delete_item(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.menu.delete_item', data=data)

    @classmethod
    async def get_all_menu_item(cls, data: Dict) -> Dict:
        return await cls._call_rpc('restaurant.menu.get_all_menu_item', data=data)
