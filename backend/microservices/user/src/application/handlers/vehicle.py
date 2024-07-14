from application.interfaces.vehicle import (
    SubmitVehicleRequest, SubmitVehicleResponse,
    GetVehicleInfoRequest, GetVehicleInfoResponse,
)
from domain.user import UserDomain

class VehicleService:

    @staticmethod
    async def submit_vehicle(request: SubmitVehicleRequest) -> SubmitVehicleResponse:
        user = await UserDomain.load(request.user_id)
        vehicle_id = await user.(
            user_id=request.user_id,
            # Add other fields as required
        )
        return SubmitVehicleResponse(success=True, vehicle_id=vehicle_id)

    @staticmethod
    async def get_vehicle_info(request: GetVehicleInfoRequest) -> GetVehicleInfoResponse:
        vehicle_info = await VehicleDomain.get_vehicle_info(user_id=request.user_id)
        return GetVehicleInfoResponse(
            # Populate the response fields accordingly
        )
