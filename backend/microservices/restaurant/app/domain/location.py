import h3
from data_access.repository.location import LocationRepository
from typing import List, Optional
from schemas.location import LocationSchema, IndexedLocationSchema
from config.h3 import HEXAGON_RESOLUTION, K_RING_RADIUS
from data_access.repository.status import StatusRepository
from config.location import MAXIMUM_LOCATION_TO_STORE_PER_DRIVER, LOCATIONS_CACHE_TTL


class DriverLocationHandler:
    @staticmethod
    def encode_location(latitude: float, longitude: float, resolution: int = HEXAGON_RESOLUTION):
        return h3.geo_to_h3(latitude, longitude, resolution=resolution)

    @staticmethod
    def get_h3_ring(h3_index: str, k=K_RING_RADIUS):
        return h3.k_ring(h3_index, k=k)

    @classmethod
    async def save_driver_locations(cls, driver_id: str, locations: List[LocationSchema]):
        h3_locations = []
        for location in locations:
            h3_locations.append(
                dict(
                    h3_index=cls.encode_location(location.latitude, location.longitude),
                    timestamp=location.timestamp,
                )
            )
        await LocationRepository.save_driver_locations(driver_id, h3_locations, ttl=LOCATIONS_CACHE_TTL)

    @classmethod
    async def load_driver_locations(cls, driver_id: str):
        stored_locations = await LocationRepository.load_driver_locations(driver_id)
        return stored_locations

    @classmethod
    async def get_nearest_drivers(cls, location: LocationSchema, radius: int = 100, maximum_drivers_count: Optional[int] = None):
        h3_index = cls.encode_location(location.latitude, location.longitude)
        h3_neigbors = cls.get_h3_ring(h3_index)

        query_indices = [h3_index] + h3_neigbors
        drivers = await LocationRepository.load_ids_within_hexagons(query_indices)

        if maximum_drivers_count:
            drivers = drivers[:maximum_drivers_count]
        return drivers
