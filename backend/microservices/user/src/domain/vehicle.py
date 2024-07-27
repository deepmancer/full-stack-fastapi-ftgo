from typing import Optional, List, Dict, Any

from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.utc_time import timezone as tz

from domain import get_logger
from data_access.repository import DatabaseRepository
from models.vehicle import VehicleInfo
from utils import handle_exception


class VehicleDomain:
    def __init__(
        self,
        vehicle_id: str,
        driver_id: str,
        plate_number: str,
        license_number: str,
        created_at: str,
        updated_at: Optional[str],
    ):
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id
        self.plate_number = plate_number
        self.license_number = license_number
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def _from_schema(vehicle_schema: VehicleInfo) -> "VehicleDomain":
        return VehicleDomain(
            vehicle_id=vehicle_schema.id,
            driver_id=vehicle_schema.driver_id,
            plate_number=vehicle_schema.plate_number,
            license_number=vehicle_schema.license_number,
            created_at=vehicle_schema.created_at.astimezone(tz) if vehicle_schema.created_at else None,
            updated_at=vehicle_schema.updated_at.astimezone(tz) if vehicle_schema.updated_at else None,
        )

    @staticmethod
    async def load(
        driver_id: str,
        vehicle_id: str,
        raise_error_on_missing: bool = True,
    ) -> Optional["VehicleDomain"]:
        try:
            vehicle_schema = await DatabaseRepository.fetch_by_query(VehicleInfo, query={"id": vehicle_id}, one_or_none=True)
            if not vehicle_schema:
                if raise_error_on_missing:
                    raise BaseError(ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload={"driver_id": driver_id, "vehicle_id": vehicle_id})
                return None
            
            vehicle = VehicleDomain._from_schema(vehicle_schema)
            if vehicle.driver_id != driver_id:
                raise BaseError(
                    ErrorCodes.VEHICLE_PERMISSION_DENIED_ERROR,
                    payload={"driver_id": driver_id, "vehicle_id": vehicle_id},
                )
            return vehicle
        except Exception as e:
            payload = {"vehicle_id": vehicle_id}
            get_logger().error(ErrorCodes.VEHICLE_GET_ERROR, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_GET_ERROR, payload=payload)

    @staticmethod
    async def load_driver_vehicle(driver_id: str) -> Optional["VehicleDomain"]:
        try:
            vehicle_schema = await DatabaseRepository.fetch_by_query(VehicleInfo, query={"driver_id": driver_id}, one_or_none=True)
            if not vehicle_schema:
                raise BaseError(ErrorCodes.VEHICLE_NOT_FOUND_ERROR, payload={"driver_id": driver_id})
            return VehicleDomain._from_schema(vehicle_schema)
        except Exception as e:
            payload = {"driver_id": driver_id}
            get_logger().error(ErrorCodes.VEHICLE_GET_ERROR, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_GET_ERROR, payload=payload)

    @staticmethod
    async def register_vehicle(driver_id: str, plate_number: str, license_number: str) -> Optional["VehicleDomain"]:
        try:
            new_vehicle = VehicleInfo(
                driver_id=driver_id,
                plate_number=plate_number,
                license_number=license_number,
            )
            new_vehicle = await DatabaseRepository.insert(new_vehicle)
            return VehicleDomain._from_schema(new_vehicle)
        except Exception as e:
            payload = {
                "driver_id": driver_id,
                "plate_number": plate_number,
                "license_number": license_number,
            }
            get_logger().error(ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_SUBMISSION_ERROR, payload=payload)

    async def delete(self):
        try:
            await DatabaseRepository.delete_by_query(VehicleInfo, query={"id": self.vehicle_id})
        except Exception as e:
            payload = {"vehicle_id": self.vehicle_id}
            get_logger().error(ErrorCodes.VEHICLE_REMOVE_ERROR, payload=payload)
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
            updated_vehicle = await DatabaseRepository.update_by_query(VehicleInfo, query={"id": self.vehicle_id}, update_fields=update_fields)
            self._update_from_schema(updated_vehicle)
            return update_fields
        except Exception as e:
            payload = {
                "driver_id": self.driver_id,
                "vehicle_id": self.vehicle_id,
                "update_fields": update_fields,
            }
            get_logger().error(ErrorCodes.VEHICLE_MODIFY_ERROR, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.VEHICLE_MODIFY_ERROR, payload=payload)

    def get_info(self) -> Dict[str, Any]:
        return {
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
            "plate_number": self.plate_number,
            "license_number": self.license_number,
        }

    def _update_from_schema(self, vehicle_schema: VehicleInfo):
        vehicle = VehicleDomain._from_schema(vehicle_schema)
        self.vehicle_id = vehicle.vehicle_id
        self.driver_id = vehicle.driver_id
        self.plate_number = vehicle.plate_number
        self.license_number = vehicle.license_number
        self.created_at = vehicle.created_at
        self.updated_at = vehicle.updated_at
