from typing import Dict

from services.base import Microservice


class LocationService(Microservice):
    _service_name = 'location'

    @classmethod
    async def submit_location(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.location.submit', data=data)

    @classmethod
    async def change_status_online(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.status.online', data=data)

    @classmethod
    async def change_status_offline(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.status.offline', data=data)

    @classmethod
    async def get_nearest_drivers(cls, data: Dict) -> Dict:
        return await cls._call_rpc('location.drivers.get_nearest', data=data)

    @classmethod
    async def get_last_location(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.location.get', data=data)

    @classmethod
    async def get_driver_status(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.status.get', data=data)
