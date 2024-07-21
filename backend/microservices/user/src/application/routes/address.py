import os
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError

from application import get_logger
from application.schema import *
from domain.user import UserDomain

router = APIRouter(prefix="/address", tags=["address"])


@router.post("/add", response_model=AddressResponse)
async def add_address(request: AddAddressRequest):
    try:
        user = await UserDomain.load(request.user_id)
        address_id = await user.add_address(
            request.address_line_1, request.address_line_2, request.city, request.postal_code, request.country
        )
        return AddressResponse(address_id=address_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while adding address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.delete("/delete", response_model=DeleteAddressResponse)
async def delete_address(user_id: str, address_id: str):
    try:
        user = await UserDomain.load(user_id)
        await user.delete_address(address_id)
        return DeleteAddressResponse(address_id=address_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while deleting address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.post("/set-preferred", response_model=SetPreferredAddressResponse)
async def set_address_as_default(request: SetPreferredAddressRequest):
    try:
        user = await UserDomain.load(request.user_id)
        await user.set_address_as_default(request.address_id)
        return SetPreferredAddressResponse(address_id=request.address_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while setting preferred address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.get("/get_info", response_model=AddressInfoResponse)
async def get_address_info(user_id: str, address_id: str):
    try:
        user = await UserDomain.load(user_id)
        address = await user.get_address_info(address_id)
        return AddressInfoResponse(
            address_id=address.address_id,
            is_default=address.is_default,
            address_line_1=address.address_line_1,
            address_line_2=address.address_line_2,
            city=address.city,
            postal_code=address.postal_code,
            country=address.country,
        )
    except Exception as e:
        get_logger().error(f"Error occurred while getting address info: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.get("/get_all_info", response_model=AllAddressesResponse)
async def get_all_addresses(user_id: str):
    try:
        user = await UserDomain.load(user_id)
        addresses = await user.get_addresses_info()
        return AllAddressesResponse(addresses=addresses)
    except Exception as e:
        get_logger().error(f"Error occurred while getting all addresses: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))