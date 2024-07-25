import asyncio
from typing import Any, Dict, List, Optional

from ftgo_utils.errors import ErrorCodes

from data_access.repository import DatabaseRepository
from config import DomainError
from domain.user import UserDomain
from domain import get_logger, layer_name
from models import VehicleInfo
from utils.error_handler import handle_error

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
            get_logger().error(f"Error while registering vehicle for user {self.user.id}: {e}")
            return handle_error(e=e, error_code=ErrorCodes.DB_INSERT_ERROR, layer=layer_name)
    
    async def get_vehicle_info(self) -> Dict[str, str]:
        try:
            vehicle_info = await DatabaseRepository.fetch_by_query(VehicleInfo, {"driver_id": self.user.id}, one_or_none=True)
            return DriverDomain.vehicle_dict(vehicle_info)
        except Exception as e:
            get_logger().error(f"Error while fetching vehicle for user {self.user.id}: {e}")
            return handle_error(e=e, error_code=ErrorCodes.DB_FETCH_ERROR, layer=layer_name)

    @staticmethod
    def vehicle_dict(vehicle: VehicleInfo):
        if not vehicle:
            return None
        return dict(
            vehicle_id=vehicle.id,
            driver_id=vehicle.driver_id,
            plate_number=vehicle.plate_number,
            license_number=vehicle.license_number,
        )
