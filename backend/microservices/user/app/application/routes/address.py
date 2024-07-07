import os
from loguru import logger
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from application.schema import (
    AddAddressRequest, AddressResponse,
    DeleteAddressRequest, DeleteAddressResponse,
    SetPreferredAddressRequest, SetPreferredAddressResponse,
    AddressInfoRequest, AddressInfoResponse,
    AllAddressesRequest, AllAddressesResponse,
)
from domain.user import UserDomain

router = APIRouter(prefix="/address", tags=["address"])

@router.post("/add", response_model=AddressResponse)
async def add_address(request: AddAddressRequest):
    try:
        user = await UserDomain.load(request.user_id, request.access_token)
        address_id = await user.add_address(
            request.address_line_1, request.address_line_2, request.city, request.postal_code, request.country
        )
        return AddressResponse(address_id=address_id)
    except Exception as e:
        logger.error(f"Error occurred while adding address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.delete("/delete", response_model=DeleteAddressResponse)
async def delete_address(request: DeleteAddressRequest):
    try:
        user = await UserDomain.load(request.user_id, request.access_token)
        await user.delete_address(request.address_id)
        return DeleteAddressResponse(address_id=request.address_id)
    except Exception as e:
        logger.error(f"Error occurred while deleting address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.post("/set-preferred", response_model=SetPreferredAddressResponse)
async def set_address_as_default(request: SetPreferredAddressRequest):
    try:
        user = await UserDomain.load(request.user_id, request.access_token)
        await user.set_address_as_default(request.address_id)
        return SetPreferredAddressResponse(address_id=request.address_id)
    except Exception as e:
        logger.error(f"Error occurred while setting preferred address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

# two get apis, one for get address info (input is address id, user id, and access token)
# another for get all addresses of a user (input is user id and access token)

@router.get("/get_info", response_model=AddressInfoResponse)
async def get_address_info(request: AddressInfoRequest):
    try:
        user = await UserDomain.load(request.user_id, request.access_token)
        address = await user.get_address_info(request.address_id)
        return address
    except:
        logger.error(f"Error occurred while getting address info: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.get("/get_all_info", response_model=AllAddressesResponse)
async def get_all_addresses(request: AllAddressesRequest):
    try:
        user = await UserDomain.load(request.user_id, request.access_token)
        addresses = await user.get_addresses_info()
        return AllAddressesResponse(addresses=addresses)
    except Exception as e:
        logger.error(f"Error occurred while getting all addresses: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
