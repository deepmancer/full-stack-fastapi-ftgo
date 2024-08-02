from typing import Any, Dict, Optional

from ftgo_utils.errors import ErrorCodes

from domain import get_logger
from domain.assets import VehicleDomain
from domain.user import User
from utils import handle_exception

class Driver(User):
    def __init__(
        self,
        user_id: str,
        role: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        hashed_password: str,
        gender: Optional[str] = None,
        email: Optional[str] = None,
        created_at: Optional[str] = None,
        verified_at: Optional[str] = None,
        last_login_time: Optional[str] = None,
        national_id: Optional[str] = None,
    ):
        super().__init__(
            user_id=user_id,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            hashed_password=hashed_password,
            gender=gender,
            email=email,
            created_at=created_at,
            verified_at=verified_at,
            last_login_time=last_login_time,
            national_id=national_id,
        )
        self.vehicle: Optional[VehicleDomain] = None

    async def load_private_attributes(self) -> None:
        try:
            self.vehicle = await VehicleDomain.load_driver_vehicle(driver_id=self.user_id, raise_error_on_missing=False)
        except Exception as e:
            payload = {"user_id": self.user_id}
            get_logger().error(ErrorCodes.VEHICLE_LOAD_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_LOAD_ERROR, payload=payload)

    def get_vehicle_info(self) -> Optional[Dict[str, Any]]:
        if self.vehicle:
            return self.vehicle.get_info()
        return {}


    async def register_vehicle(self, plate_number: str, license_number: str) -> Optional[Dict[str, Any]]:
        try:
            vehicle = await VehicleDomain.register_vehicle(
                driver_id=self.user_id,
                plate_number=plate_number,
                license_number=license_number,
            )
            self.vehicle = vehicle
            return vehicle.get_info()
        except Exception as e:
            payload = {
                'user_id': self.user_id,
                'plate_number': plate_number,
                'license_number': license_number
            }
            get_logger().error(ErrorCodes.VEHICLE_SUBMISSION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)

    async def delete_vehicle(self) -> Dict:
        try:
            if self.vehicle:
                await self.vehicle.delete()
                vehicle_id = self.vehicle.vehicle_id
                self.vehicle = None
                return vehicle_id
            return {}
        except Exception as e:
            payload = {'user_id': self.user_id}
            get_logger().error(ErrorCodes.VEHICLE_REMOVE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_REMOVE_ERROR, payload=payload)
