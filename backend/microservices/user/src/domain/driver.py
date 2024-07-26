import asyncio
from typing import Any, Dict, List, Optional

from ftgo_utils.errors import ErrorCodes

from data_access.repository import DatabaseRepository
from config import DomainError
from domain.user import UserDomain
from domain import get_logger
from models import VehicleInfo
from utils.exception import handle_exception

class DriverDomain(UserDomain):
    async def register_vehicle_data(self, plate_number: str, license_number: str):
        try:
            vehicle_info = VehicleInfo(
                driver_id=self.user.id,
                plate_number=plate_number,
                license_number=license_number,
            )
            vehicle_info = await DatabaseRepository.insert(vehicle_info)
            return DriverDomain.vehicle_dict(vehicle_info)
        except Exception as e:
            payload = dict(user_id=self.user.id, plate_number=plate_number, license_number=license_number)
            get_logger().error(ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)

    async def get_vehicle_info(self) -> Optional[Dict[str, str]]:
        try:
            vehicle_info = await DatabaseRepository.fetch_by_query(VehicleInfo, {"driver_id": self.user.id}, one_or_none=True)
            return DriverDomain.vehicle_dict(vehicle_info)
        except Exception as e:
            payload = dict(user_id=self.user.id)
            get_logger().error(ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload=payload)

    @staticmethod
    def vehicle_dict(vehicle: VehicleInfo) -> Optional[Dict[str, str]]:
        if not vehicle:
            return None
        return dict(
            vehicle_id=vehicle.id,
            driver_id=vehicle.driver_id,
            plate_number=vehicle.plate_number,
            license_number=vehicle.license_number,
        )
