from application.dependencies import AccessManager
from application.exceptions import handle_exception
from application.schemas.common import SuccessResponse
from application.schemas.driver.location import LocationsSchema, LocationPointMixin
from fastapi import APIRouter, Request, Depends
from ftgo_utils.enums import ResponseStatus, Roles
from ftgo_utils.errors import BaseError, ErrorCodes
from services.location import LocationService

router = APIRouter(
    prefix='/location',
    tags=["driver_location_service"],
    dependencies=[Depends(AccessManager([Roles.DRIVER]))],
)

@router.post("/submit", response_model=SuccessResponse)
async def submit_location(request: Request, request_data: LocationsSchema):
    try:
        data = {
            "driver_id": request.state.user.user_id,
            "locations": request_data.dict().get('locations', []),
        }
        response = await LocationService.submit_location(data=data)
        status = response.get('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()

        error_code = ErrorCodes.get_error_code(response.get('error_code'))
        raise BaseError(
            error_code=error_code,
            message="Submitting location failed",
            payload=request_data.dict(),
        )
    except Exception as e:
        await handle_exception(
            request, e, default_failure_message="Submitting location failed"
        )


@router.get("/get", response_model=LocationPointMixin)
async def get_location(request: Request):
    try:
        driver_id = request.state.user.user_id
        response = await LocationService.get_last_location(data={"driver_id": driver_id})
        status = response.get('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return LocationPointMixin(
                latitude=response.get("latitude"),
                longitude=response.get("longitude"),
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting location failed",
            payload={"driver_id": driver_id},
        )
    except Exception as e:
        await handle_exception(
            request, e, default_failure_message="Getting last location failed"
        )
