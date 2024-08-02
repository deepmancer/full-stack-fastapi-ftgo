from typing import Dict
from services.base import Microservice

class VehicleService(Microservice):
    _service_name = 'vehicle'

    @classmethod
    async def register(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.vehicle.register', data=data)

    @classmethod
    async def get_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.vehicle.get_info', data=data)

    @classmethod
    async def delete(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.vehicle.delete', data=data)

