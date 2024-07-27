import asyncio
from typing import Any, Dict, Optional

from ftgo_utils.errors import ErrorCodes, BaseError

from domain import get_logger
from domain.vehicle import VehicleDomain
from domain.user import UserDomain
from models import VehicleInfo
from utils import handle_exception

logger = get_logger()

class DriverDomain(UserDomain):
    async def register_vehicle(self, plate_number: str, license_number: str) -> Optional[Dict[str, Any]]:
        try:
            vehicle = await VehicleDomain.register_vehicle(
                driver_id=self.user_id,
                plate_number=plate_number,
                license_number=license_number,
            )
            return vehicle.get_info()
        except Exception as e:
            payload = {
                'user_id': self.user_id,
                'plate_number': plate_number,
                'license_number': license_number
            }
            logger.error(ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)

    async def get_vehicle_info(self) -> Optional[Dict[str, str]]:
        try:
            vehicle = await VehicleDomain.load_driver_vehicle(driver_id=self.user_id)
            return vehicle.get_info()
        except Exception as e:
            payload = {'user_id': self.user_id}
            logger.error(ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload=payload)

    async def delete_vehicle(self):
        try:
            vehicle = await VehicleDomain.load_driver_vehicle(driver_id=self.user_id)
            await vehicle.delete()
        except Exception as e:
            payload = {'user_id': self.user_id}
            logger.error(ErrorCodes.VEHICLE_REMOVE_ERROR, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_REMOVE_ERROR, payload=payload)
