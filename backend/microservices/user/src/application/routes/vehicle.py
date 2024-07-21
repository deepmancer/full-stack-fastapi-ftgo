import os
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger
from application.schema import *
from domain.user import UserDomain
from domain.driver import DriverDomain

router = APIRouter(prefix="/vehicle", tags=["driver_vehicle"])

@router.post("/register", response_model=SubmitVehicleResponse, status_code=status.HTTP_201_CREATED)
async def register_vehicle(request: SubmitVehicleRequest):
    try:
        driver = await DriverDomain.load(request.user_id)
        vehicle_id = await driver.submit_vehicle_data(
            plate_number=request.plate_number,
            license_number=request.license_number,
        )
        return SubmitVehicleResponse(vehicle_id=vehicle_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while registering driver's vehicle: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/get_info", response_model=GetVehicleInfoResponse)
async def verify_account(request: GetVehicleInfoRequest):
    try:
        driver = await DriverDomain.load(request.user_id)
        vehicle_info = await driver.get_vehicle_info(
            plate_number=request.plate_number,
            license_number=request.license_number,
        )
        return GetVehicleInfoResponse(
            vehicle_id=vehicle_info.id,
            plate_number=vehicle_info.plate_number,
            license_number=vehicle_info.license_number,
        )
    except Exception as e:
        get_logger().error(f"Error occurred while fetching driver's vehicle information: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
