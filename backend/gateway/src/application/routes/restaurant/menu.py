import os
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger
from application.schemas.user import UserStateSchema
from application.exceptions import handle_exception
from application.schemas.restaurant.menu import (
    AddMenuItemRequest, AddMenuItemResponse, GetMenuItemInfoRequest, GetMenuItemInfoResponse,
    UpdateMenuItemRequest, UpdateMenuItemResponse, DeleteMenuItemRequest, DeleteMenuItemResponse,
    GetAllMenuItemRequest, GetAllMenuItemResponse,
)
from ftgo_utils.enums import ResponseStatus
from services.menu import MenuService
from ftgo_utils.errors import BaseError, ErrorCodes

router = APIRouter(prefix='/menu', tags=["menu"])
logger = get_logger()


@router.post("/add", response_model=AddMenuItemResponse)
async def add_item(request_data: AddMenuItemRequest):
    try:
        data = request_data.dict()

        response = await MenuService.add_item(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return AddMenuItemResponse(
                **response,
            )
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Adding menu item failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request_data, e, default_failure_message="Adding menu item failed")
        raise


@router.get("/get_info", response_model=GetMenuItemInfoResponse)
async def get_info(request: Request, request_data: GetMenuItemInfoRequest):

    try:
        data = request_data.dict()
        response = await MenuService.get_item_info(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return GetMenuItemInfoResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Get menu item info failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Get menu item info failed")
        raise


@router.put("/update", response_model=UpdateMenuItemResponse)
async def update_item(request: Request, request_data: UpdateMenuItemRequest):
    try:
        data = request_data.dict()
        response = await MenuService.update_item(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return UpdateMenuItemResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Update menu item info failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Update menu item info failed")
        raise


@router.delete("/delete", response_model=DeleteMenuItemResponse)
async def delete_item(request: Request, request_data: DeleteMenuItemRequest):
    try:
        data = request_data.dict()
        response = await MenuService.delete_item(data=data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return DeleteMenuItemResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Delete menu item info failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Delete menu item info failed")
        raise

@router.post("/get_all_menu_item", response_model=GetAllMenuItemResponse)
async def get_all_menu_item(request: Request, request_data: GetAllMenuItemRequest):
    try:
        data = request_data.dict()
        response = await MenuService.get_all_menu_item(data=data)

        status = response.pop('status', ResponseStatus.ERROR.value)
        if status == ResponseStatus.SUCCESS.value:
            return GetAllMenuItemResponse(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Getting all menus failed",
            payload={"data": data},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Getting all menus failed")
        raise