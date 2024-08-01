from typing import List, Optional

from config import LocationConfig
from data_access.repository import DatabaseRepository, CacheRepository
from ftgo_utils.logger import get_logger
from ftgo_utils.errors import ErrorCodes, BaseError
from utils import handle_exception
from domain.geo_location import GeoLocation
from domain.hexagon import Hexagon
from dto import DriverLocationDTO

class DriverLocation:
    def __init__(self, driver_id: str, locations: List[GeoLocation] = []):
        self.driver_id: str = driver_id
        self.locations: List[GeoLocation] = locations

    @property
    def config(self) -> LocationConfig:
        return LocationConfig()

    async def get_valid_locations(self) -> List[GeoLocation]:
        valid_locations = [loc for loc in self.locations if loc.is_valid()]
        last_location = await self.load_last_location()
        if last_location:
            valid_locations.append(last_location)
        sorted_locations = sorted(valid_locations, key=lambda x: x.timestamp, reverse=True)
        return sorted_locations[:self.config.keep_last_locations_count]

    async def persist_locations(self):
        try:
            locations = await self.get_valid_locations()
            locations_dto = [
                DriverLocationDTO(
                    driver_id=self.driver_id,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    timestamp=location.timestamp,
                    accuracy=location.accuracy,
                    speed=location.speed,
                    bearing=location.bearing,
                )
                for location in locations
            ]
            await DatabaseRepository.insert(locations_dto)
        except Exception as e:
            payload = {"driver_id": self.driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_SAVE_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_SAVE_ERROR, payload=payload)

    async def update_hexagon_cache(self) -> None:
        try:
            locations = await self.get_valid_locations()
            if not locations:
                return
            most_recent_location = locations[0]
            last_hex_id = await Hexagon.get_last_hexagon_for_driver(self.driver_id)
            current_hex_id = Hexagon.from_location(most_recent_location).hex_id
            if not last_hex_id or last_hex_id != current_hex_id:
                await Hexagon.invalidate_driver_cache(self.driver_id)
                await Hexagon.set_last_hexagon_for_driver(self.driver_id, most_recent_location)
                await Hexagon.add_driver_to_hexagon(self.driver_id, most_recent_location)
        except Exception as e:
            payload = {"driver_id": self.driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_SAVE_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_SAVE_ERROR, payload=payload)

    async def cache_locations(self):
        try:
            locations = await self.get_valid_locations()
            if not locations:
                return
            most_recent_location = locations[0]
            cache_key = self.config.cache_key
            cache = CacheRepository.get_cache(cache_key)
            await cache.insert(self.driver_id, most_recent_location.to_dict(), ttl=self.config.cache_ttl)
        except Exception as e:
            payload = {"driver_id": self.driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_SAVE_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_SAVE_ERROR, payload=payload)

    async def load_last_location(self, raise_error_on_missing: Optional[bool] = False) -> Optional[GeoLocation]:
        try:
            cache_key = self.config.cache_key
            cache = CacheRepository.get_cache(cache_key)

            location_dict = await cache.fetch(self.driver_id)
            if location_dict is None:
                if raise_error_on_missing:
                    raise BaseError(
                        error_code=ErrorCodes.LOCATION_NOT_FOUND_ERROR,
                        payload={"driver_id": self.driver_id},
                    )
                return None

            location = GeoLocation.from_dict(location_dict)
            return location
        except Exception as e:
            payload = {"driver_id": self.driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_LOAD_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_LOAD_ERROR, payload=payload)

    async def save_locations(self):
        try:
            await self.persist_locations()
            await self.cache_locations()
            await self.update_hexagon_cache()
        except Exception as e:
            payload = {"driver_id": self.driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_SAVE_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_SAVE_ERROR, payload=payload)

    async def delete_locations(self):
        try:
            await Hexagon.invalidate_driver_cache(self.driver_id)
            cache_key = self.config.cache_key
            cache = CacheRepository.get_cache(cache_key)
            await cache.delete(self.driver_id)
        except Exception as e:
            payload = {"driver_id": self.driver_id, "error": str(e)}
            get_logger().error(ErrorCodes.LOCATION_DELETE_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_DELETE_ERROR, payload=payload)
