import os
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger

from application.schemas.restaurant.restaurant import (
    RegisterRestaurantRequest, RegisterRestaurantResponse,
    GetRestaurantInfoResponse, DeleteRestaurantResponse
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

@router.delete("/delete", response_model=DeleteRestaurantResponse)
async def delete_account(request: Request):
    try:
        user: UserSchema = request.state.user
        response = await RestaurantService.delete_restaurant(data={"restaurant_id": user.restaurant_id})
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.get('error_message', 'Restaurant deletion failed')
            )
        return DeleteRestaurantResponse(success=True)
    except Exception as e:
        logger.error(f"Error occurred while deleting the restaurant: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": str(e)})
        )
