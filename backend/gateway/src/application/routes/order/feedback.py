from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from application import get_logger
from application.dependencies import AccessManager
from application.exceptions import handle_exception
from application.schemas.common import EmptyResponse, SuccessResponse
from ftgo_utils.enums import ResponseStatus, Roles
from ftgo_utils.errors import BaseError, ErrorCodes
from services.feedback import FeedbackService

from application.schemas.order.feedback import (
    CreateDeliveryRatingRequest, CreateDeliveryRatingResponse, UpdateDeliveryRatingRequest, UpdateDeliveryRatingResponse,
    GetDeliveryRatingRequest, GetDeliveryRatingResponse, GetCustomerDeliveryRatingsRequest, GetCustomerDeliveryRatingsResponse,
    GetDriverDeliveryRatingsRequest, GetDriverDeliveryRatingsResponse,
    CreateOrderRatingRequest, CreateOrderRatingResponse, UpdateOrderRatingRequest, UpdateOrderRatingResponse,
    GetOrderRatingRequest, GetOrderRatingResponse, GetCustomerOrderRatingsRequest, GetCustomerOrderRatingsResponse,
    GetRestaurantOrderRatingsRequest, GetRestaurantOrderRatingsResponse
)

router = APIRouter(
    prefix='/feedback',
    tags=["feedback"],
    dependencies=[Depends(AccessManager([Roles.CUSTOMER, Roles.RESTAURANT_ADMIN]))],
)
logger = get_logger()

# Delivery Rating Endpoints

@router.post("/delivery/rating/create", response_model=CreateDeliveryRatingResponse)
async def create_delivery_rating(request: Request, request_data: CreateDeliveryRatingRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.create_delivery_rating(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return CreateDeliveryRatingResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Creating delivery rating failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Creating delivery rating failed")

@router.put("/delivery/rating/update", response_model=UpdateDeliveryRatingResponse)
async def update_delivery_rating(request: Request, request_data: UpdateDeliveryRatingRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.update_delivery_rating(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return UpdateDeliveryRatingResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Updating delivery rating failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Updating delivery rating failed")

@router.get("/delivery/rating/get", response_model=GetDeliveryRatingResponse)
async def get_delivery_rating(request: Request, request_data: GetDeliveryRatingRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id
        response = await FeedbackService.get_delivery_rating(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return GetDeliveryRatingResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting delivery rating failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting delivery rating failed")

@router.get("/delivery/rating/customer", response_model=GetCustomerDeliveryRatingsResponse)
async def get_customer_delivery_ratings(request: Request, request_data: GetCustomerDeliveryRatingsRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.get_customer_delivery_ratings(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return GetCustomerDeliveryRatingsResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting customer delivery ratings failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting customer delivery ratings failed")

@router.get("/delivery/rating/driver", response_model=GetDriverDeliveryRatingsResponse)
async def get_driver_delivery_ratings(request: Request, request_data: GetDriverDeliveryRatingsRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.get_driver_delivery_ratings(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return GetDriverDeliveryRatingsResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting driver delivery ratings failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting driver delivery ratings failed")

# Order Rating Endpoints

@router.post("/order/rating/create", response_model=CreateOrderRatingResponse)
async def create_order_rating(request: Request, request_data: CreateOrderRatingRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.create_order_rating(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return CreateOrderRatingResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Creating order rating failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Creating order rating failed")

@router.put("/order/rating/update", response_model=UpdateOrderRatingResponse)
async def update_order_rating(request: Request, request_data: UpdateOrderRatingRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.update_order_rating(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return UpdateOrderRatingResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Updating order rating failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Updating order rating failed")

@router.get("/order/rating/get", response_model=GetOrderRatingResponse)
async def get_order_rating(request: Request, request_data: GetOrderRatingRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.get_order_rating(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return GetOrderRatingResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting order rating failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting order rating failed")

@router.get("/order/rating/customer", response_model=GetCustomerOrderRatingsResponse)
async def get_customer_order_ratings(request: Request, request_data: GetCustomerOrderRatingsRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.get_customer_order_ratings(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return GetCustomerOrderRatingsResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting customer order ratings failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting customer order ratings failed")

@router.get("/order/rating/restaurant", response_model=GetRestaurantOrderRatingsResponse)
async def get_restaurant_order_ratings(request: Request, request_data: GetRestaurantOrderRatingsRequest):
    try:
        data = request_data.dict()
        data['customer_id'] = request.state.user.user_id

        response = await FeedbackService.get_restaurant_order_ratings(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return GetRestaurantOrderRatingsResponse(**response)

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting restaurant order ratings failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting restaurant order ratings failed")
