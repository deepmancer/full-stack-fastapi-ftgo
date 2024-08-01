import asyncio
from typing import List, Optional

from config import DriverStatusConfig
from data_access.repository import DatabaseRepository, CacheRepository
from domain.geo_location import GeoLocation
from domain.driver_location import DriverLocation
from domain.hexagon import Hexagon
from ftgo_utils.enums import DriverStatus, DriverAvailabilityStatus
from ftgo_utils.errors import ErrorCodes, BaseError
from ftgo_utils.logger import get_logger
from utils import handle_exception

class Driver:
    def __init__(self, driver_id: str, status: Optional[str] = None, availability: Optional[str] = None):
        self.driver_id = driver_id
        self.status = status
        self.availability = availability

    @property
    def config(self) -> DriverStatusConfig:
        return DriverStatusConfig()

    @classmethod
    def get_status_cache(cls) -> CacheRepository:
        status_config = DriverStatusConfig()
        return CacheRepository.get_cache(status_config.cache_key)

    def is_available(self) -> bool:
        return self.availability == DriverAvailabilityStatus.AVAILABLE.value and self.is_online()
    
    def is_online(self) -> bool:
        return self.status == DriverStatus.ONLINE.value

    @staticmethod
    async def load(driver_id: str) -> Optional["Driver"]:
        try:
            status_cache = Driver.get_status_cache()
            status_dict = await status_cache.fetch(driver_id)
            if not status_dict or 'status' not in status_dict:
                status = DriverStatus.OFFLINE.value
                availability = DriverAvailabilityStatus.AVAILABLE.value
                status_dict = {"status": status, "availability": availability}
                await status_cache.insert(driver_id, status_dict, ttl=DriverStatusConfig().cache_ttl)
            return Driver(driver_id=driver_id, status=status_dict['status'], availability=status_dict['availability'])
        except Exception as e:
            payload = {"driver_id": driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.DRIVER_STATUS_LOAD_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.DRIVER_STATUS_LOAD_ERROR, payload=payload)

    @staticmethod
    async def get_nearest_drivers(
        latitude: float,
        longitude: float,
        radius_m: int = 100,
        max_driver_count: Optional[int] = None,
    ) -> List[str]:
        try:
            nearest_drivers = await Hexagon.get_nearest_drivers(latitude, longitude, radius_m)
            if max_driver_count:
                nearest_drivers = nearest_drivers[:max_driver_count]
                
            driver_ids = [driver_data["driver_id"] for driver_data in nearest_drivers]
            drivers = await asyncio.gather(*[Driver.load(driver_id) for driver_id in driver_ids])
            nearest_available_drivers = []
            for driver, driver_data in zip(drivers, nearest_drivers):
                if driver and driver.is_available():
                    nearest_available_drivers.append(driver_data)
            return nearest_available_drivers
        except Exception as e:
            payload = {"latitude": latitude, "longitude": longitude, "error": str(e)}
            get_logger().error(ErrorCodes.GET_NEAREST_DRIVERS_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.GET_NEAREST_DRIVERS_ERROR, payload=payload)
    
    async def submit_locations(self, locations: List[dict]):
        try:
            geo_locations = [GeoLocation.from_dict(loc) for loc in locations]
            driver_location = DriverLocation(driver_id=self.driver_id, locations=geo_locations)
            if self.status == DriverStatus.OFFLINE.value:
                await driver_location.delete_locations()
                status_cache = Driver.get_status_cache()
                await status_cache.insert(
                    self.driver_id, 
                    {'status': DriverStatus.ONLINE.value, 'availability': self.availability},
                    ttl=self.config.cache_ttl
                )
                self.status = DriverStatus.ONLINE.value
            else:
                await driver_location.save_locations()
        except Exception as e:
            payload = {"driver_id": self.driver_id, "locations": [location.to_dict() for location in locations], "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_SAVE_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_SAVE_ERROR, payload=payload)

    async def _update_cache(self, status: Optional[str] = None, availability: Optional[str] = None):
        status_cache = Driver.get_status_cache()
        cache_data = {'status': status or self.status, 'availability': availability or self.availability}
        await status_cache.insert(self.driver_id, cache_data, ttl=self.config.cache_ttl)

    async def change_status(self, status: str):
        try:
            if status == self.status:
                return
            driver_location = DriverLocation(driver_id=self.driver_id)
            await driver_location.delete_locations()
            await self._update_cache(status=status)
            self.status = status
            self.availability = DriverAvailabilityStatus.AVAILABLE.value
        except Exception as e:
            payload = {"driver_id": self.driver_id, "status": status, "error": str(e)}
            get_logger().error(ErrorCodes.DRIVER_CHANGE_STATUS_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.DRIVER_CHANGE_STATUS_ERROR, payload=payload)

    async def change_availability(self, availability: str):
        try:
            if availability == self.availability:
                return
            await self._update_cache(availability=availability)
            self.availability = availability
        except Exception as e:
            payload = {"driver_id": self.driver_id, "availability": availability, "error": str(e)}
            get_logger().error(ErrorCodes.DRIVER_CHANGE_STATUS_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.DRIVER_CHANGE_STATUS_ERROR, payload=payload)

    async def get_location(self) -> GeoLocation:
        try:
            driver_location = DriverLocation(driver_id=self.driver_id)
            return await driver_location.load_last_location(raise_error_on_missing=True)
        except Exception as e:
            payload = {"driver_id": self.driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_LOAD_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_LOAD_ERROR, payload=payload)

    def get_status(self) -> str:
        return self.status

    def get_availability(self) -> str:
        return self.availability

    async def get_last_location(self) -> dict:
        location = await self.get_location()
        return location.to_dict()

    def get_info(self) -> dict:
        return {
            "driver_id": self.driver_id,
            "status": self.status,
        }
