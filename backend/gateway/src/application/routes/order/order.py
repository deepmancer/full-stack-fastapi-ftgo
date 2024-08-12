from fastapi import APIRouter, Request, Depends
from application.exceptions import handle_exception
from ftgo_utils.enums import ResponseStatus, Roles
from ftgo_utils.errors import BaseError, ErrorCodes
from application.schemas.common import SuccessResponse
from application.schemas.order.order import (
    CreateOrderRequest, GetOrderHistoryRequest, GetOrderHistoryResponse,
    UpdateOrderRequest, ConfirmOrderRequest, RejectOrderRequest
)
from services.order import OrderService
from application.dependencies import AccessManager

router = APIRouter(
    prefix='/order',
    tags=["order_service"],
    dependencies=[Depends(AccessManager([Roles.DRIVER]))],
)

@router.post("/history", response_model=GetOrderHistoryResponse)
async def get_order_history(request: Request, request_data: GetOrderHistoryRequest):
    try:
        data = {
            "order_id": request_data['order_id'],
        }
        response = await OrderService.get_order_history(data=data)
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



@router.post("/create", response_model=SuccessResponse)
async def create_order(request: Request, request_data: CreateOrderRequest):
    try:
        data = {
            "customer_id": request.state.user.user_id,
            "restaurant_id": request_data['restaurant_id'],
            "order_items": request_data['items'],
        }
        response = await OrderService.create_order(data=data)
        status = response.get('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()

        error_code = ErrorCodes.get_error_code(response.get('error_code'))
        raise BaseError(
            error_code=error_code,
            message="Creating order failed",
            payload=request_data.dict(),
        )
    except Exception as e:
        await handle_exception(
            request, e, default_failure_message="Creating order failed"
        )


@router.post("/update", response_model=SuccessResponse)
async def update_order(request: Request, request_data: UpdateOrderRequest):
    try:
        data = {
            "customer_id": request.state.user.user_id,
            "restaurant_id": request_data['restaurant_id'],
            "order_items": request_data['items'],
        }
        response = await OrderService.create_order(data=data)
        status = response.get('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()

        error_code = ErrorCodes.get_error_code(response.get('error_code'))
        raise BaseError(
            error_code=error_code,
            message="Creating order failed",
            payload=request_data.dict(),
        )
    except Exception as e:
        await handle_exception(
            request, e, default_failure_message="Creating order failed"
        )


@router.post("/confirm", response_model=SuccessResponse)
async def restaurant_confirm(request: Request, request_data: ConfirmOrderRequest):
    try:
        data = {
            "order_id": request_data['order_id'],
            "restaurant_id": request_data['restaurant_id'],
        }
        response = await OrderService.create_order(data=data)
        status = response.get('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()

        error_code = ErrorCodes.get_error_code(response.get('error_code'))
        raise BaseError(
            error_code=error_code,
            message="Confirming order failed",
            payload=request_data.dict(),
        )
    except Exception as e:
        await handle_exception(
            request, e, default_failure_message="Confirming order failed"
        )


@router.post("/reject", response_model=SuccessResponse)
async def restaurant_reject(request: Request, request_data: RejectOrderRequest):
    try:
        data = {
            "order_id": request_data['order_id'],
            "restaurant_id": request_data['restaurant_id'],
        }
        response = await OrderService.create_order(data=data)
        status = response.get('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()

        error_code = ErrorCodes.get_error_code(response.get('error_code'))
        raise BaseError(
            error_code=error_code,
            message="Rejecting order failed",
            payload=request_data.dict(),
        )
    except Exception as e:
        await handle_exception(
            request, e, default_failure_message="Rejecting order failed"
        )