import asyncio
from typing import Any, Dict, List, Optional

from data_access.repository import DatabaseRepository
from domain.user import UserDomain

from domain.exceptions import *
from domain import get_logger
from models import VehicleInfo


class DriverDomain(UserDomain):
    async def submit_vehicle_data(self, plate_number: str, license_number: str):
        try:
            vehicle_info = VehicleInfo(
                driver_id=self.user.id,
                plate_number=plate_number,
                license_number=license_number,
            )
            vehicle_info = await DatabaseRepository.insert(vehicle_info)
            return vehicle_info.id
        except Exception as e:
            raise VehicleRegisterError(user_id=self.user_id, message=str(e))
    
    async def get_vehicle_info(self) -> Dict[str, str]:
        try:
            vehicle_info = await DatabaseRepository.fetch_by_query(VehicleInfo, {"driver_id": self.user.id}, one_or_none=True)
            return {
                "vehicle_id": vehicle_info.id,
                "plate_number": vehicle_info.plate_number,
                "license_number": vehicle_info.license_number,
            }
        except Exception as e:
            raise VehicleNotFoundError(user_id=self.user_id, message=str(e))
