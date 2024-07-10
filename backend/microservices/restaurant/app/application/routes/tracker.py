from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application.validators import (
    validate_timestamp, validate_speed, validate_accuracy, validate_uuid, validate_status
)
from application import get_logger
from domain.location import LocationDomain
from application.schema import (
    DriverLocationSchema, SubmitLocationRequest, SubmitLocationResponse, 
    ChangeStatusRequest, ChangeStatusResponse, GetNearestDriversRequest, 
    GetNearestDriversResponse
)

router = APIRouter(prefix="/tracker", tags=["tracker"])

@router.get("/get_nearest_drivers", response_model=GetNearestDriversResponse)
async def get_nearest_drivers(request: GetNearestDriversRequest):
    try:
        nearest_drivers = await LocationDomain.get_nearest_drivers(
            location=request.location,
            radius=request.radius,
            max_count=request.max_count
        )
        return GetNearestDriversResponse(driver_locations=nearest_drivers)
    except Exception as e:
        get_logger().error(f"Error occurred while getting nearest drivers: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
