import os
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger

from application.schemas.restaurant.restaurant import (
    RegisterRestaurantRequest, RegisterRestaurantResponse,
    GetRestaurantInfoResponse, DeleteRestaurantResponse
)
from application.schemas.user import UserSchema
from ftgo_utils.enums import ResponseStatus
from services.restaurant import RestaurantService

router = APIRouter(prefix='/restaurant', tags=["restaurant"])
logger = get_logger()

@router.post("/register", response_model=RegisterRestaurantResponse)
async def register(request: Request, request_data: RegisterRestaurantRequest):
    try:
        user: UserSchema = request.state.user
        response = await RestaurantService.register(
            data={
                "owner_user_id": user.user_id,
                "name": request_data.name,
                "postal_code": request_data.postal_code,
                "address": request_data.address,
                "address_lat": request_data.address_lat,
                "address_lng": request_data.address_lng,
                "restaurant_licence_id": request_data.restaurant_licence_id,
            }
        )
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.get('error_message', 'Restaurant registration failed')
            )
        return RegisterRestaurantResponse(restaurant_id=response["restaurant_id"])
    except Exception as e:
        logger.error(f"Error occurred while registering the restaurant: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": str(e)})
        )

@router.get("/supplier_restaurant_info", response_model=GetRestaurantInfoResponse)
async def get_supplier_restaurant_info(request: Request):
    try:
        user: UserSchema = request.state.user
        response = await RestaurantService.get_supplier_restaurant_info(data={"user_id": user.user_id})
        if response.get('status', ResponseStatus.ERROR.value) == ResponseStatus.ERROR.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.get('error_message', 'Get restaurant information failed')
            )
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
    except Exception as e:
        logger.error(f"Error occurred while getting the restaurant info: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": str(e)})
        )

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
