from typing import Dict, Any

from domain.driver import DriverDomain

class VehicleService:
    @staticmethod
    async def register_vehicle(user_id: str, plate_number: str, license_number: str, **kwargs) -> Dict[str, Any]:
        driver = await DriverDomain.load(user_id)
        vehicle_info = await driver.register_vehicle(
            plate_number=plate_number,
            license_number=license_number,
        )
        return vehicle_info

    @staticmethod
    async def get_vehicle_info(user_id: str, **kwargs) -> Dict[str, Any]:
        driver = await DriverDomain.load(user_id)
        vehicle_info = await driver.get_vehicle_info()
        return vehicle_info
        
    @staticmethod
    async def delete_vehicle(user_id: str, **kwargs) -> Dict[str, Any]:
        driver = await DriverDomain.load(user_id)
        await driver.delete_vehicle()
        return {}
