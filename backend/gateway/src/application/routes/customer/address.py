from application.dependencies import AccessManager
from application.exceptions import handle_exception
from application.schemas.account.address import (
        AddressIdSchema, AddressesSchema, AddressIdPreferencySchema
)
from application.schemas.common import SuccessResponse
from application.schemas.user import UserStateSchema
from fastapi import APIRouter, Request, Depends
from ftgo_utils.enums import ResponseStatus, Roles
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.schemas import (
        AddressMixin, AddressInfoMixin
)
from services.user import UserService

router = APIRouter(
    prefix='/address',
    tags=["user_address"],
    dependencies=[Depends(AccessManager([Roles.CUSTOMER]))],
)

@router.get("/get_all_info", response_model=AddressesSchema)
async def get_all_addresses(request: Request):
    try:
        user: UserStateSchema = request.state.user
        response = await UserService.get_all_addresses(data={"user_id": user.user_id})

        status = response.pop('status', ResponseStatus.ERROR.value)
        if status == ResponseStatus.SUCCESS.value:
            return AddressesSchema(addresses=response["addresses"])

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting all addresses failed",
            payload={"user_id": user.user_id},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting all addresses failed")
        raise


@router.post("/add", response_model=AddressMixin)
async def add_address(request: Request, request_data: AddressInfoMixin):
    try:
        user: UserStateSchema = request.state.user
        data = request_data.dict()
        data.update({"user_id": user.user_id})
        response = await UserService.add_address(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return AddressMixin(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Adding address failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Adding address failed")
        raise


@router.delete("/delete", response_model=SuccessResponse)
async def delete_address(request: Request, request_data: AddressIdSchema):
    try:
        user: UserStateSchema = request.state.user
        data = request_data.dict()
        data.update({"user_id": user.user_id})
        response = await UserService.delete_address(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Deleting address failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Deleting address failed")
        raise


@router.post("/set-preferred", response_model=AddressMixin)
async def set_address_preferency(request: Request, request_data: AddressIdPreferencySchema):
    try:
        user: UserStateSchema = request.state.user
        data = request_data.dict()
        data.update({"user_id": user.user_id, "set_default": True})
        response = await UserService.set_preferred_address(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return AddressMixin(
                # user_id=user.user_id,
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Setting address as preferred failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Setting address as preferred failed")
        raise
