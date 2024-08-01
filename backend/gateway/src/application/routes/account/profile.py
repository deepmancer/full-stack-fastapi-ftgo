from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from application import get_logger
from application.exceptions import handle_exception
from application.schemas.common import EmptyResponse, SuccessResponse
from application.schemas.user import UserStateSchema
from config import AuthConfig
from domain.token_manager import TokenManager
from ftgo_utils.enums import ResponseStatus, Roles
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.schemas import UserInfoMixin
from services.user import UserService
from application.dependencies import AccessManager

router = APIRouter(
    prefix='/profile',
    tags=["user_profile"],
    dependencies=[Depends(AccessManager([Roles.CUSTOMER, Roles.ADMIN, Roles.DRIVER, Roles.RESTAURANT_ADMIN]))],
)
logger = get_logger()

@router.post("/logout", response_model=SuccessResponse)
async def logout(request: Request):
    try:
        user: UserStateSchema = request.state.user
        response = await UserService.logout(data={"user_id": user.user_id})
        
        if response.get('status') == ResponseStatus.SUCCESS.value:
            await TokenManager().invalidate_token(user.token)
            return SuccessResponse()
        
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Logout failed",
            payload={"user_id": user.user_id},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Logout failed")

@router.get("/user_info", response_model=UserInfoMixin)
async def get_info(request: Request):
    try:
        user: UserStateSchema = request.state.user

        response = await UserService.get_profile_info(data={"user_id": user.user_id})
        
        if response.get('status') == ResponseStatus.SUCCESS.value:
            return UserInfoMixin(
                first_name=response.get("first_name"),
                last_name=response.get("last_name"),
                phone_number=response.get("phone_number"),
                national_id=response.get("national_id"),
                role=response.get("role"),
                gender=response.get("gender"),
                email=response.get("email"),
            )
        
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Get user information failed",
            payload={"user_id": user.user_id},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Get user information failed")

@router.delete("/delete", response_model=SuccessResponse)
async def delete_account(request: Request):
    try:
        user: UserStateSchema = request.state.user
        response = await UserService.delete_account(data={"user_id": user.user_id})
        
        if response.get('status') == ResponseStatus.SUCCESS.value:
            await TokenManager().invalidate_token(user.token)
            return SuccessResponse()
        
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Account deletion failed",
            payload={"user_id": user.user_id},
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Account deletion failed")