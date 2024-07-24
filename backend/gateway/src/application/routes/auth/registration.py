from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from ftgo_utils.logger import get_logger
from services import UserService
from ftgo_utils.enums import ResponseStatus
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from config import AuthConfig
from data_access.repository import CacheRepository
from ftgo_utils.jwt_auth import encode

from application.schemas.routes.registration import (
    RegisterSchema, UserIdSchema, AuthenticateAccountSchema, UserIdVerifiedSchema,
    AuthCodeSchema, LoginSchema, TokenSchema,
)


router = APIRouter(prefix='/auth', tags=["user_profile"])
logger = get_logger()

@router.post("/register", response_model=UserIdSchema, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterSchema):
    try:
        data = request.dict()
        response = await UserService.create_profile(data)
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=response.get('error_message', 'Registration failed'))
        return UserIdSchema(user_id=response["user_id"], auth_code=response["auth_code"])
    except Exception as e:
        logger.error(f"Error occurred while registering user: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/verify", response_model=UserIdVerifiedSchema)
async def verify_account(request: AuthenticateAccountSchema):
    try:
        data = request.dict()
        response = await UserService.verify_account(data)
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get('error_message', 'Account verification failed'))
        return UserIdVerifiedSchema(success=response["success"])
    except Exception as e:
        logger.error(f"Error occurred while verifying the account: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/resend_code", response_model=AuthCodeSchema)
async def resend_auth_code(request: UserIdSchema):
    try:
        data = request.dict()
        response = await UserService.resend_auth_code(data)
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get('error_message', 'Resending auth code failed'))
        return AuthCodeSchema(auth_code=response["auth_code"])
    except Exception as e:
        logger.error(f"Error occurred while resending the auth code: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/login", response_model=TokenSchema)
async def login(request: LoginSchema):
    try:
        data = request.dict()
        response = await UserService.login(data)
        if response.get('status') == ResponseStatus.ERROR.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get('error_message', 'Login failed'))

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
        
        return TokenSchema(user_id=response['user_id'], token=token)
    except Exception as e:
        logger.error(f"Error occurred while logging the user in: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
