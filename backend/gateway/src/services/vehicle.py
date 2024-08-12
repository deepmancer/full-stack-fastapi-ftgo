from typing import Dict

from services.base import Microservice


class VehicleService(Microservice):
    _service_name = 'vehicle'

    @classmethod
    async def register(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.vehicle.register', data=data)

    @classmethod
    async def get_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.vehicle.get_info', data=data)

    @classmethod
    async def delete(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.vehicle.delete', data=data)

