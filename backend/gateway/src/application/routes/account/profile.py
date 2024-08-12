from application import get_logger
from application.dependencies import AccessManager
from application.exceptions import handle_exception
from application.schemas.account.profile import UpdateUserRequest, UserInfo
from application.schemas.common import SuccessResponse
from application.schemas.user import UserStateSchema
from domain.token_manager import TokenManager
from fastapi import APIRouter, Request, Depends
from ftgo_utils.enums import ResponseStatus, Roles
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.schemas import UserInfoMixin
from services.user import UserService

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
                # email=response.get("email"),
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



@router.put("/update", response_model=UserInfo)
async def update_profile(request: Request, request_data: UpdateUserRequest):
    try:
        user: UserStateSchema = request.state.user
        data = request_data.dict()
        data.update({"user_id": user.user_id})
        response = await UserService.update_profile(data=data)

        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return UserInfo(
                **response,
            )

        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Update user info failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(Request, e, default_failure_message="Update user info failed")