from application.interfaces.vehicle import (
    SubmitVehicleRequest, SubmitVehicleResponse,
    GetVehicleInfoRequest, GetVehicleInfoResponse,
)
from domain.driver import DriverDomain

class VehicleService:

    @staticmethod
    async def register_vehicle(request: SubmitVehicleRequest) -> SubmitVehicleResponse:
        user = await DriverDomain.load(request.user_id)
        vehicle_info = await user.register_vehicle_data(
            plate_number=request.plate_number,
            license_number=request.license_number,
        )
        return SubmitVehicleResponse(success=True, **vehicle_info)

    @staticmethod
    async def get_vehicle_info(request: GetVehicleInfoRequest) -> GetVehicleInfoResponse:
        vehicle_info = await VehicleDomain.get_vehicle_info(user_id=request.user_id)
        return GetVehicleInfoResponse(**vehicle_info)
