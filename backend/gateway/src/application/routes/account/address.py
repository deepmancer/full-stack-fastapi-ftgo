import os
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger
from application.schemas.account.address import (
    AllAddressesResponse,
    AddAddressRequest, AddAddressResponse,
    DeleteAddressRequest, DeleteAddressResponse,
    SetPreferredAddressRequest, SetPreferredAddressResponse,
)
from application.schemas.user import UserSchema
from ftgo_utils.enums import ResponseStatus
from services.user import UserService

router = APIRouter(prefix='/address', tags=["user_address"])
logger = get_logger()

@router.get("/get_all_info", response_model=AllAddressesResponse)
async def get_all_addresses(request: Request):
    try:
        user: UserSchema = request.state.user
        response = await UserService.get_all_addresses(data={"user_id": user.user_id})
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=response.get('error_message', 'Getting All Addresses has been failed'))
        return AllAddressesResponse(addresses=response["addresses"])
    except Exception as e:
        get_logger().error(f"Error occurred while getting all addresses: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/add", response_model=AddAddressResponse)
async def add_address(request: Request, add_address_request: AddAddressRequest):
    try:

        user: UserSchema = request.state.user
        response = await UserService.add_address(data={"user_id": user.user_id,
                                                       "address_line_1": add_address_request.address_line_1,
                                                       "address_line_2": add_address_request.address_line_2,
                                                       "city": add_address_request.city,
                                                       "postal_code": add_address_request.postal_code,
                                                       "country": add_address_request.country})
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=response.get('error_message', 'Adding Address has been failed'))
        return AddAddressResponse(address_id=response["address_id"])
    except Exception as e:
        get_logger().error(f"Error occurred while adding address: {e}", request=add_address_request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))


@router.delete("/delete", response_model=DeleteAddressResponse)
async def delete_address(request: Request, delete_address_request: DeleteAddressRequest):
    try:
        user: UserSchema = request.state.user
        response = await UserService.delete_address(data={"user_id": user.user_id,
                                                          'address_id': delete_address_request.address_id})

        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=response.get('error_message', 'Deleting Address has been failed'))
        return DeleteAddressResponse(address_id=delete_address_request.address_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while deleting address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/set-preferred", response_model=SetPreferredAddressResponse)
async def set_address_as_default(request: Request, set_address_preferred_request: SetPreferredAddressRequest):
    try:
        user: UserSchema = request.state.user

        response = await UserService.set_preferred_address(data={"user_id": user.user_id,
                                                                 'address_id': set_address_preferred_request.address_id})

        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=response.get('error_message', 'Setting Address As Preferred has been failed'))

        return SetPreferredAddressResponse(address_id=response['address_id'], success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while setting preferred address: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))