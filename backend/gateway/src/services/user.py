from typing import Dict

from services.base import Microservice


class UserService(Microservice):
    _service_name = 'user'

    @classmethod
    async def create_profile(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.create', data=data)

    @classmethod
    async def add_address(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.address.add_address', data=data)

    @classmethod
    async def register_vehicle(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.vehicle.register', data=data)

    @classmethod
    async def resend_auth_code(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.resend_auth_code', data=data)

    @classmethod
    async def verify_account(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.verify_account', data=data)

    @classmethod
    async def login(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.login', data=data)

    @classmethod
    async def get_profile_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.get_info', data=data)

    @classmethod
    async def delete_account(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.delete_account', data=data)

    @classmethod
    async def logout(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.logout', data=data)

    @classmethod
    async def update_profile(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.profile.update_profile', data=data)

    @classmethod
    async def get_default_address(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.address.get_default_address', data=data)

    @classmethod
    async def delete_address(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.address.delete', data=data)

    @classmethod
    async def set_preferred_address(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.address.set_preferred_address', data=data)

    @classmethod
    async def get_address_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.address.get_address_info', data=data)

    @classmethod
    async def get_all_addresses(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.address.get_all_addresses', data=data)

    @classmethod
    async def update_information(cls, data: Dict) -> Dict:
        return await cls._call_rpc('user.address.update_information', data=data)

    @classmethod
    async def get_vehicle_info(cls, data: Dict) -> Dict:
        return await cls._call_rpc('driver.vehicle.get_info', data=data)