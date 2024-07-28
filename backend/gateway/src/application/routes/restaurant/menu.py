import os
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger
from application.schemas.restaurant.menu import (
    AddMenuItemResponse, GetMenuItemInfoResponse, UpdateMenuItemResponse, DeleteMenuItemResponse
)
from ftgo_utils.enums import ResponseStatus
from services.restaurant import RestaurantService

router = APIRouter(prefix='/menu', tags=["menu"])
logger = get_logger()

@router.post("/add", response_model=AddMenuItemResponse)
async def add_item(request: Request):
    try:
        data = await request.json()
        response = await RestaurantService.add_item(
            name=data['name'],
            price=data['price'],
            description=data.get('description')
        )
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.get('error_message', 'Adding menu item failed')
            )
        return AddMenuItemResponse(item_id=response["item_id"])
    except Exception as e:
        logger.error(f"Error occurred while adding the menu item: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": str(e)})
        )

@router.get("/info/{item_id}", response_model=GetMenuItemInfoResponse)
async def get_info(item_id: str):
    try:
        response = await RestaurantService.get_item_info(item_id=item_id)
        if response.pop('status', ResponseStatus.ERROR.value) == ResponseStatus.ERROR.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.get('error_message', 'Get menu item information failed')
            )
        return GetMenuItemInfoResponse(
            name=response.get("name"),
            price=response.get("price"),
            description=response.get("description")
        )
    except Exception as e:
        logger.error(f"Error occurred while getting the menu item info: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": str(e)})
        )

@router.put("/update/{item_id}", response_model=UpdateMenuItemResponse)
async def update_item(item_id: str, request: Request):
    try:
        data = await request.json()
        response = await RestaurantService.update_item(
            item_id=item_id,
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description')
        )
        if response.pop('status', ResponseStatus.ERROR.value) == ResponseStatus.ERROR.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.get('error_message', 'Update menu item failed')
            )
        return UpdateMenuItemResponse(
            name=response.get("name"),
            price=response.get("price"),
            description=response.get("description")
        )
    except Exception as e:
        logger.error(f"Error occurred while updating the menu item: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": str(e)})
        )

@router.delete("/delete/{item_id}", response_model=DeleteMenuItemResponse)
async def delete_item(item_id: str):
    try:
        response = await RestaurantService.delete_item(item_id=item_id)
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.get('error_message', 'Delete menu item failed')
            )
        return DeleteMenuItemResponse(success=True)
    except Exception as e:
        logger.error(f"Error occurred while deleting the menu item: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": str(e)})
        )
