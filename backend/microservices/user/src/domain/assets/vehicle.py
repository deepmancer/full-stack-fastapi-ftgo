from typing import Any, Dict, Optional

from ftgo_utils import uuid_gen
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.utc_time import timezone as tz

from data_access.repository import DatabaseRepository
from domain import get_logger
from dto import VehicleDTO
from utils import handle_exception


class VehicleDomain:
    def __init__(
        self,
        vehicle_id: str,
        driver_id: str,
        plate_number: str,
        license_number: str,
        created_at: str,
    ):
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id
        self.plate_number = plate_number
        self.license_number = license_number
        self.created_at = created_at

    @staticmethod
    async def load(
        driver_id: str,
        vehicle_id: str,
        raise_error_on_missing: bool = True,
    ) -> Optional["VehicleDomain"]:
        try:
            vehicle = await DatabaseRepository.fetch(VehicleDTO, query={"id": vehicle_id}, one_or_none=True)
            if not vehicle:
                if raise_error_on_missing:
                    raise BaseError(ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload={"driver_id": driver_id, "vehicle_id": vehicle_id})
                return None
            
            vehicle = VehicleDomain.from_dto(vehicle)
            if vehicle.driver_id != driver_id:
                raise BaseError(
                    ErrorCodes.VEHICLE_PERMISSION_DENIED_ERROR,
                    payload={"driver_id": driver_id, "vehicle_id": vehicle_id},
                )
            return vehicle
        except Exception as e:
            payload = {"vehicle_id": vehicle_id}
            get_logger().error(ErrorCodes.VEHICLE_GET_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_GET_ERROR, payload=payload)

    @staticmethod
    async def load_driver_vehicle(driver_id: str, raise_error_on_missing: bool = True) -> Optional["VehicleDomain"]:
        try:
            vehicle = await DatabaseRepository.fetch(VehicleDTO, query={"driver_id": driver_id}, one_or_none=True)
            if not vehicle:
                if raise_error_on_missing:
                    raise BaseError(ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload={"driver_id": driver_id})
                return None
            return VehicleDomain.from_dto(vehicle)
        except Exception as e:
            payload = {"driver_id": driver_id}
            get_logger().error(ErrorCodes.VEHICLE_GET_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_GET_ERROR, payload=payload)

    @staticmethod
    async def register_vehicle(driver_id: str, plate_number: str, license_number: str) -> Optional["VehicleDomain"]:
        try:
            vehicle_id = uuid_gen.uuid4()
            new_vehicle = VehicleDTO(
                vehicle_id=vehicle_id,
                driver_id=driver_id,
                plate_number=plate_number,
                license_number=license_number,
            )
            new_vehicle = await DatabaseRepository.insert(new_vehicle)
            return VehicleDomain.from_dto(new_vehicle)
        except Exception as e:
            payload = {
                "driver_id": driver_id,
                "plate_number": plate_number,
                "license_number": license_number,
            }
            get_logger().error(ErrorCodes.VEHICLE_SUBMISSION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)

    async def delete(self) -> str:
        try:
            await DatabaseRepository.delete(VehicleDTO, query={"id": self.vehicle_id})
            return self.vehicle_id
        except Exception as e:
            payload = {"vehicle_id": self.vehicle_id}
            get_logger().error(ErrorCodes.VEHICLE_REMOVE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_REMOVE_ERROR, payload=payload)

    async def update_information(
        self,
        plate_number: Optional[str] = None,
        license_number: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        update_fields = {}
        if plate_number:
            update_fields["plate_number"] = plate_number
        if license_number:
            update_fields["license_number"] = license_number

        try:
            updated_vehicle = await DatabaseRepository.update(VehicleDTO, query={"id": self.vehicle_id}, update_fields=update_fields)
            self.update_from_dto(updated_vehicle)
            return self.get_info()
        except Exception as e:
            payload = {
                "driver_id": self.driver_id,
                "vehicle_id": self.vehicle_id,
                "update_fields": update_fields,
            }
            get_logger().error(ErrorCodes.VEHICLE_MODIFY_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_MODIFY_ERROR, payload=payload)
            return None

    def get_info(self) -> Dict[str, Any]:
        info = {
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
            "plate_number": self.plate_number,
            "license_number": self.license_number,
        }
        return {k: v for k, v in info.items() if v is not None}

    @staticmethod
    def from_dto(vehicle: VehicleDTO) -> "VehicleDomain":
        return VehicleDomain(
            vehicle_id=vehicle.vehicle_id,
            driver_id=vehicle.driver_id,
            plate_number=vehicle.plate_number,
            license_number=vehicle.license_number,
            created_at=vehicle.created_at.astimezone(tz) if vehicle.created_at else None,
        )

    def update_from_dto(self, vehicle: VehicleDTO) -> None:
        self.vehicle_id = vehicle.id
        self.driver_id = vehicle.driver_id
        self.plate_number = vehicle.plate_number
        self.license_number = vehicle.license_number
        self.created_at = vehicle.created_at.astimezone(tz) if vehicle.created_at else None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, VehicleDomain) and self.vehicle_id == other.vehicle_id
