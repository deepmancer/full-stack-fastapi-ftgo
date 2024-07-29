from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from application.exceptions import handle_exception
from application.schemas.auth.registration import (
    UserAuthCodeSchema, UpdateProfileSchema, UserIdMixin, LoginSchema, RegistrationSchema, LoggedInUserSchema
)
from application.schemas.common import EmptyResponse, SuccessResponse
from ftgo_utils.schemas import (
    UserIdMixin, UserInfoMixin, UserMixin
)

from config import AuthConfig
from data_access.repository import CacheRepository
from ftgo_utils.enums import ResponseStatus
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.jwt_auth import encode
from ftgo_utils.logger import get_logger
from services import UserService

router = APIRouter(prefix='/auth', tags=["user_profile"])
logger = get_logger()

@router.post("/register", response_model=UserAuthCodeSchema, status_code=status.HTTP_201_CREATED)
async def register(request: Request, request_data: RegistrationSchema):
    try:
        data = request_data.dict()
        response = await UserService.create_profile(data)

        status = response.pop('status', ResponseStatus.ERROR.value)
        if status == ResponseStatus.SUCCESS.value:
            return UserAuthCodeSchema(
                user_id=response["user_id"],
                auth_code=response["auth_code"],
            )
        
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="User registration failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="User registration failed")

@router.post("/verify", response_model=SuccessResponse)
async def verify_account(request: Request, request_data: UserAuthCodeSchema):
    try:
        data = request_data.dict()
        response = await UserService.verify_account(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return SuccessResponse()
        
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Account verification failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Account verification failed")

@router.post("/resend_code", response_model=UserAuthCodeSchema)
async def resend_auth_code(request: Request, request_data: UserIdMixin):
    try:
        data = request_data.dict()
        response = await UserService.resend_auth_code(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            return UserAuthCodeSchema(auth_code=response["auth_code"], user_id=data["user_id"])
        
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Resending auth code failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Resending auth code failed")

@router.post("/login", response_model=LoggedInUserSchema)
async def login(request: Request, request_data: LoginSchema):
    try:
        data = request_data.dict()
        response = await UserService.login(data)
        status = response.pop('status', ResponseStatus.ERROR.value)

        if status == ResponseStatus.SUCCESS.value:
            payload = {
                "user_id": response['user_id'],
                "phone_number": response['phone_number'],
                "role": response["role"],
                "hashed_password": response["hashed_password"],
            }
            auth_config = AuthConfig()
            access_token_expires = timedelta(minutes=auth_config.access_token_expire_minutes)
            token = encode(
                payload=payload,
                secret=auth_config.secret,
                algorithm=auth_config.algorithm,
                expiration=access_token_expires.total_seconds()
            )
  
            token_cache = CacheRepository.get_cache(auth_config.cache_key_prefix)
            await token_cache.set(
                key=token,
                value=payload,
                ttl=int(access_token_expires.total_seconds()),
            )

            return LoggedInUserSchema(**response, token=token)
        
        raise BaseError(
            error_code=ErrorCodes.get_error_code(response.get('error_code')),
            message="Login failed",
            payload=data,
        )
    except Exception as e:
        await handle_exception(request, e, default_failure_message="Login failed")
