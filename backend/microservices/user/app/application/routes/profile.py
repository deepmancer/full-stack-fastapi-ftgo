import os
from loguru import logger
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from application.schema import (
    RegisterRequest, RegisterResponse,
    AuthenticateAccountRequest, AuthenticateAccountResponse,
    LoginRequest, LoginResponse,
    DeleteProfileRequest, DeleteProfileResponse,
    DeleteAllAddressesRequest, DeleteAllAddressesResponse,
    LogoutRequest, LogoutResponse,
    GetUserInfoRequest, GetUserInfoResponse,
)
from domain.user import UserDomain

router = APIRouter(prefix="/profile", tags=["user_profile"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    try:
        user_id, auth_code = await UserDomain.register(
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            password=request.password,
            role=request.role,
            national_id=request.national_id,
        )
        return RegisterResponse(user_id=user_id, auth_code=auth_code)
    except Exception as e:
        logger.error(f"Error occurred while registering user: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/verify_account", response_model=AuthenticateAccountResponse)
async def verify_account(request: AuthenticateAccountRequest):
    try:
        user_id = await UserDomain.verify_account(request.user_id, request.auth_code)
       
        return AuthenticateAccountResponse(user_id=user_id)
    except Exception as e:
        logger.error(f"Error occurred while verifying the account: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        access_token = await UserDomain.login(request.phone_number, request.password, request.role)
        return LoginResponse(access_token=access_token)
    except Exception as e:
        logger.error(f"Error occurred while logging the user in: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

# logout api
@router.post("/logout", response_model=LogoutResponse)
async def logout(request: LogoutRequest):
    try:
        user = await UserDomain.load(request.user_id)
        await user.logout()
        return LogoutResponse(success=True)
    except Exception as e:
        logger.error(f"Error occurred while logging the user out: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.get("/get_user_info", response_model=GetUserInfoResponse)
async def get_info(request: GetUserInfoRequest):
    try:
        user = await UserDomain.load(request.user_id)
        user_info = user.get_info()
        return GetUserInfoResponse(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            phone_number=user_info["phone_number"],
            gender=user_info["gender"],
            role=user_info["role"],
        )

    except Exception as e:
        logger.error(f"Error occurred while getting the user info: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.delete("/delete_account", response_model=DeleteProfileResponse)
async def delete_account(request: DeleteProfileRequest):
    try:
        user = await UserDomain.load(request.user_id)
        await user.delete_account()
        return DeleteProfileResponse(success=True)
    except Exception as e:
        logger.error(f"Error occurred while deleting the account: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
