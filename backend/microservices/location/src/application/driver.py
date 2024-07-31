from typing import Dict, Any, List
from application import get_logger
from ftgo_utils.enums import DriverStatus, DriverAvailabilityStatus

from domain.driver import Driver

class DriverService:
    @staticmethod
    async def submit_location(
        driver_id: str,
        locations: List[Dict[str, Any]],
        **kwargs,
    ) -> Dict[str, Any]:
        driver = await Driver.load(driver_id)
        await driver.submit_locations(
            locations=locations,
        )
        return {}

    @staticmethod
    async def change_status_online(driver_id: str, **kwargs) -> Dict[str, Any]:
        driver = await Driver.load(driver_id)
        await driver.change_status(DriverStatus.ONLINE.value)
        return {}

    @staticmethod
    async def change_status_offline(driver_id: str, **kwargs) -> Dict[str, Any]:
        driver = await Driver.load(driver_id)
        await driver.change_status(DriverStatus.OFFLINE.value)
        return {}

    @staticmethod
    async def set_driver_available(driver_id: str, **kwargs) -> Dict[str, Any]:
        driver = await Driver.load(driver_id)
        await driver.change_availability(DriverAvailabilityStatus.AVAILABLE.value)
        return {}

    @staticmethod
    async def set_driver_occupied(driver_id: str, **kwargs) -> Dict[str, Any]:
        driver = await Driver.load(driver_id)
        await driver.change_availability(DriverAvailabilityStatus.OCCUPIED.value)
        return {}
