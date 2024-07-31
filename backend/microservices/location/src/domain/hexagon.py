from typing import List, Optional, Dict, Any
from data_access.repository import DatabaseRepository, CacheRepository
from ftgo_utils.logger import get_logger
from ftgo_utils.constants import SIUnits
from ftgo_utils.errors import ErrorCodes
from domain.geo_location import GeoLocation
from utils import handle_exception
from ftgo_utils.geo import get_hexagon_neighbors, haversine
from config import HexagonConfig
from ftgo_utils.constants import RadiusLengthConfig

class Hexagon:
    def __init__(self, hex_id: str, resolution: int):
        self.hex_id = hex_id
        self.resolution = resolution

    @property
    def config(self) -> HexagonConfig:
        return HexagonConfig()

    @classmethod
    def from_location(cls, location: GeoLocation) -> 'Hexagon':
        config = HexagonConfig()
        hex_id = location.get_hexagon_index(resolution=config.hexagon_resolution)
        return cls(hex_id, config.hexagon_resolution)

    @classmethod
    async def get_last_hexagon_for_driver(cls, driver_id: str) -> Optional[str]:
        try:
            cache_key = HexagonConfig().driver_hexagon_cache_key
            driver_cache = CacheRepository.get_cache(cache_key)
            hex_id = await driver_cache.fetch(driver_id)
            return hex_id
        except Exception as e:
            payload = {"driver_id": driver_id}
            get_logger().info(ErrorCodes.LOCATION_LOAD_ERROR.value, payload=payload)
            return None

    @classmethod
    async def set_last_hexagon_for_driver(cls, driver_id: str, location: GeoLocation) -> None:
        try:
            hexagon = cls.from_location(location)
            driver_cache = CacheRepository.get_cache(hexagon.config.driver_hexagon_cache_key)
            await driver_cache.insert(driver_id, hexagon.hex_id, ttl=hexagon.config.driver_hexagon_cache_ttl)
        except Exception as e:
            payload = {"driver_id": driver_id, "location": location.to_dict()}
            get_logger().error(ErrorCodes.LOCATION_SAVE_ERROR.value, payload=payload)

    @classmethod
    async def remove_last_hexagon_for_driver(cls, driver_id: str) -> None:
        try:
            cache_key = HexagonConfig().driver_hexagon_cache_key
            driver_cache = CacheRepository.get_cache(cache_key)
            await driver_cache.delete(driver_id)
        except Exception as e:
            payload = {"driver_id": driver_id}
            get_logger().info(ErrorCodes.LOCATION_DELETE_ERROR.value, payload=payload)

    @classmethod
    async def remove_driver_from_hexagon(cls, driver_id: str, hex_id: str) -> None:
        try:
            cache_key = HexagonConfig().cache_key
            hexagon_cache = CacheRepository.get_cache(cache_key)
            await hexagon_cache.delete(keys=hex_id, fields=driver_id, data_type="hash")
        except Exception as e:
            payload = {"driver_id": driver_id, "hex_id": hex_id}
            get_logger().info(ErrorCodes.LOCATION_DELETE_ERROR.value, payload=payload)

    @classmethod
    async def invalidate_driver_cache(cls, driver_id: str) -> None:
        last_hexagon_id = await cls.get_last_hexagon_for_driver(driver_id)
        if last_hexagon_id:
            await cls.remove_driver_from_hexagon(driver_id, last_hexagon_id)
        await cls.remove_last_hexagon_for_driver(driver_id)

    @classmethod
    async def add_driver_to_hexagon(cls, driver_id: str, location: GeoLocation) -> None:
        try:
            hexagon = cls.from_location(location)
            hexagon_cache = CacheRepository.get_cache(hexagon.config.cache_key)
            await hexagon_cache.insert(
                keys=hexagon.hex_id, 
                values={driver_id: location.to_dict()}, 
                data_type='hash'
            )
        except Exception as e:
            payload = {"driver_id": driver_id, "location": location.to_dict()}
            get_logger().error(ErrorCodes.LOCATION_SAVE_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.LOCATION_SAVE_ERROR, payload=payload)

    async def get_drivers(self) -> Dict[str, GeoLocation]:
        try:
            hexagon_cache = CacheRepository.get_cache(self.config.cache_key)
            drivers_cached_data = await hexagon_cache.fetch(self.hex_id, data_type='hash')
            if not drivers_cached_data:
                return {}
            return {driver_id: GeoLocation.from_dict(value) for driver_id, value in drivers_cached_data.items()}
        except Exception as e:
            payload = {"hex_id": self.hex_id}
            get_logger().error(ErrorCodes.GET_NEAREST_DRIVERS_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.GET_NEAREST_DRIVERS_ERROR, payload=payload)
    
    @staticmethod
    async def get_nearest_drivers(
        latitude: float,
        longitude: float,
        radius_m: int = 100,
    ) -> List[Dict[str, Any]]:
        try:
            geo_location = GeoLocation(latitude=latitude, longitude=longitude)
            hexagon = Hexagon.from_location(geo_location)
            drivers_data = await hexagon.get_drivers()
            flatten_drivers = [
                (driver_id, location, haversine(
                    geo_location.latitude,
                    geo_location.longitude,
                    location.latitude,
                    location.longitude,
                    unit=SIUnits.LENGTH.M
                ))
                for driver_id, location in drivers_data.items()
            ]
            nearby_drivers = [
                {
                    "driver_id": driver_id,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "distance": distance,
                }
                for driver_id, location, distance in flatten_drivers if distance <= radius_m
            ]
            sorted_drivers = sorted(nearby_drivers, key=lambda x: x["distance"])
            return sorted_drivers
        except Exception as e:
            payload = {"latitude": latitude, "longitude": longitude, "radius_m": radius_m}
            get_logger().error(ErrorCodes.GET_NEAREST_DRIVERS_ERROR.value, payload=payload)
            await handle_exception(e, ErrorCodes.GET_NEAREST_DRIVERS_ERROR, payload=payload)
