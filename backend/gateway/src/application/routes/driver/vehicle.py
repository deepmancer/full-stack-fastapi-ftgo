from application import get_logger
from application.exceptions import handle_exception
from application.schemas.driver.vehicle import (
        RegisterVehicleRequest, RegisterVehicleResponse,
        DeleteVehicleResponse, GetVehicleInfoResponse
)
from application.schemas.user import UserStateSchema
from fastapi import APIRouter, Request
from ftgo_utils.enums import ResponseStatus
from ftgo_utils.errors import BaseError, ErrorCodes
from services.vehicle import VehicleService

router = APIRouter(prefix='/vehicle', tags=["vehicle"])
logger = get_logger()


@router.post("/register", response_model=RegisterVehicleResponse)
async def register(request: Request, request_data: RegisterVehicleRequest):
    try:
        user: UserStateSchema = request.state.user

        data = request_data.dict()
        data.update({"user_id": user.user_id})
        response = await VehicleService.register(data)

        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return RegisterVehicleResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Vehicle registration failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Vehicle registration failed")


@router.get("/get_info", response_model=GetVehicleInfoResponse)
async def get_info(request: Request):
    try:
        user: UserStateSchema = request.state.user
        data = {"user_id": user.user_id}
        response = await VehicleService.get_info(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)
        if status == ResponseStatus.SUCCESS.value:
            return GetVehicleInfoResponse(
                **response
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Get vehicle info failed",
            payload={data},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Get vehicle info failed")


@router.delete("/delete", response_model=DeleteVehicleResponse)
async def delete(request: Request):
    try:
        user: UserStateSchema = request.state.user
        data = {"user_id": user.user_id}
        response = await VehicleService.delete(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return DeleteVehicleResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Delete restaurant failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Delete restaurant failed")
        raise
