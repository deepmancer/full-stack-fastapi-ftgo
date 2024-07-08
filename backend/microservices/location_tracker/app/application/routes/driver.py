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

router = APIRouter(prefix="/driver", tags=["driver"])

@router.post("/submit_location", response_model=SubmitLocationResponse)
async def submit_location(request: SubmitLocationRequest):
    try:
        await LocationDomain.submit_location(
            driver_id=request.driver_id,
            locations=request.location,
            timestamp=request.timestamp
        )
        return SubmitLocationResponse(success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while submitting location: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/change_status", response_model=ChangeStatusResponse)
async def change_status(request: ChangeStatusRequest):
    try:
        await LocationDomain.change_status(
            driver_id=request.driver_id,
            status=request.status,
            timestamp=request.timestamp
        )
        return ChangeStatusResponse(success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while changing status: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
