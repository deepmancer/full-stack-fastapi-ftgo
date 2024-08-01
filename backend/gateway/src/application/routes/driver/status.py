from fastapi import APIRouter, Request, Depends
from application.exceptions import handle_exception
from ftgo_utils.enums import ResponseStatus, Roles
from ftgo_utils.errors import BaseError, ErrorCodes
from application.schemas.common import SuccessResponse
from services.location import LocationService
from application.dependencies import AccessManager


router = APIRouter(
    prefix='/status',
    tags=["driver_location_service"],
    dependencies=[Depends(AccessManager([Roles.DRIVER]))],
)

async def change_driver_status(request: Request, status_function, success_message: str):
    try:
        driver_id = request.state.user.user_id
        response = await status_function(data={"driver_id": driver_id})
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()

        error_code = ErrorCodes.get_error_code(response.get('error_code'))
        raise BaseError(
            error_code=error_code,
            message=success_message,
            payload={"driver_id": driver_id},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message=success_message)

@router.post("/online", response_model=SuccessResponse)
async def change_status_online(request: Request):
    return await change_driver_status(
        request,
        LocationService.change_status_online,
        "Changing driver status to online failed"
    )

@router.post("/offline", response_model=SuccessResponse)
async def change_status_offline(request: Request):
    return await change_driver_status(
        request,
        LocationService.change_status_offline,
        "Changing driver status to offline failed"
    )
