from typing import Dict, Any
from application import get_logger
from domain.driver import Driver
from ftgo_utils.errors import ErrorCodes, BaseError

class TrackerService:
    @staticmethod
    async def get_nearest_drivers(location: Dict[str, Any], radius: float, max_count: int, **kwargs) -> Dict[str, Any]:
        latitude = location.get('latitude')
        longitude = location.get('longitude')
        if latitude is None or longitude is None:
            raise BaseError(
                code=ErrorCodes.INVALID_LOCATION_ERROR,
                payload={"location": location},
            )

        nearest_drivers = await Driver.get_nearest_drivers(latitude=latitude, longitude=longitude, radius_m=radius, max_driver_count=max_count)
        return {"drivers": nearest_drivers}
