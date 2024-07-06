import os
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from application.schema import (
    AddAddressRequest, AddressResponse,
    DeleteAddressRequest,
    SetPreferredAddressRequest
)
from domain.user import UserDomain

router = APIRouter(prefix="/address", tags=["address"])

@router.post("/add", response_model=AddressResponse)
async def add_address(request: AddAddressRequest):
    try:
        user = await UserDomain.from_user_id(request.user_id)
        address_id = await user.add_address(
            request.address_line_1, request.address_line_2, request.city, request.state, request.postal_code, request.country
        )
        return AddressResponse(address_id=address_id)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.delete("/delete", response_model=AddressResponse)
async def delete_address(request: DeleteAddressRequest):
    try:
        user = await UserDomain.from_user_id(request.user_id)
        address_id = await user.delete_address(request.address_id)
        return AddressResponse(address_id=address_id)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
    
@router.post("/set-preferred", response_model=AddressResponse)
async def set_address_as_default(request: SetPreferredAddressRequest):
    try:
        user = await UserDomain.from_user_id(request.user_id)
        address_id = await user.set_address_as_default(request.address_id)
        return AddressResponse(address_id=address_id)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
