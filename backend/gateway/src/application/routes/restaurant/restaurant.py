import os
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger

from application.schemas.restaurant.restaurant import (
    RegisterRestaurantRequest, RegisterRestaurantResponse,
    DeleteRestaurantRequest, DeleteRestaurantResponse,
    UpdateRestaurantRequest, UpdateRestaurantResponse,
    GetRestaurantInfoResponse, GetAllRestaurantInfoResponse
)
from application.schemas.user import UserStateSchema
from application.exceptions import handle_exception
from ftgo_utils.enums import ResponseStatus
from ftgo_utils.errors import BaseError, ErrorCodes
from services.restaurant import RestaurantService

router = APIRouter(prefix='/restaurant', tags=["restaurant"])
logger = get_logger()

@router.post("/register", response_model=RegisterRestaurantResponse)
async def register(request: Request, request_data: RegisterRestaurantRequest):
    try:
        user: UserStateSchema = request.state.user

        data = request_data.dict()
        data.update({"owner_user_id": user.user_id})
        response = await RestaurantService.register(data)

        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return RegisterRestaurantResponse(
                restaurant_id=response["restaurant_id"],
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Restaurant registration failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Restaurant registration failed")

@router.get("/get_supplier_restaurant_info", response_model=GetRestaurantInfoResponse)
async def get_supplier_restaurant_info(request: Request):
    try:
        user: UserStateSchema = request.state.user
        data = {"user_id": user.user_id}
        response = await RestaurantService.get_supplier_restaurant_info(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)
        if status == ResponseStatus.SUCCESS.value:
            return GetRestaurantInfoResponse(
                id=response.get('id'),
                owner_user_id=response.get('owner_user_id'),
                name=response.get("name"),
                postal_code=response.get("postal_code"),
                address=response.get("address"),
                address_lat=response.get("address_lat"),
                address_lng=response.get("address_lng"),
                restaurant_licence_id=response.get("restaurant_licence_id")
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Get restaurant info failed",
            payload={data},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Get restaurant info failed")


@router.get("/get_all_restaurant_info", response_model=GetAllRestaurantInfoResponse)
async def get_all_restaurant_info(request: Request):
    try:
        response = await RestaurantService.get_all_restaurant_info(data={'tmp': "tmp"})

        status = response.pop('status', ResponseStatus.ERROR.value)
        if status == ResponseStatus.SUCCESS.value:
            return GetAllRestaurantInfoResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Get all restaurant info failed",
            payload={},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Get all restaurant info failed")

@router.delete("/delete", response_model=DeleteRestaurantResponse)
async def delete_restaurant(request: Request, request_data: DeleteRestaurantRequest):
    try:
        data = request_data.dict()
        response = await RestaurantService.delete_restaurant(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return DeleteRestaurantResponse(
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


@router.put("/update", response_model=UpdateRestaurantResponse)
async def update_information(request: Request, request_data: UpdateRestaurantRequest):
    try:
        data = request_data.dict()
        response = await RestaurantService.update_information(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return UpdateRestaurantResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Update restaurant info failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Update restaurant info failed")
