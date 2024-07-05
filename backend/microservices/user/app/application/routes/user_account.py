import os
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from application.schema import (
    RegisterRequest, RegisterResponse,
    AuthenticateAccountRequest, AuthenticateAccountResponse,
    LoginRequest, LoginResponse,
    DeleteAccountRequest, DeleteAccountResponse,
    DeleteAllAddressesRequest, DeleteAllAddressesResponse
)
from domain.user import UserDomain

router = APIRouter(prefix="/account", tags=["user_account"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    try:
        user_id, auth_code = await UserDomain.register(
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            password=request.password,
            role_name=request.role_name,
        )
        return RegisterResponse(user_id=user_id, auth_code=auth_code)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/authenticate", response_model=AuthenticateAccountResponse)
async def authenticate_account(request: AuthenticateAccountRequest):
    try:
        user = await UserDomain.from_user_id(request.user_id)
        access_token, ttl = await user.authenticate(request.auth_code)
        return AuthenticateAccountResponse(access_token=access_token, access_token_ttl_seconds=ttl)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        user = await UserDomain.from_phone_number_role(request.phone_number, request.role_name)
        access_token, ttl = await user.login(request.auth_code)
        return LoginResponse(access_token=access_token, access_token_ttl_seconds=ttl)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))
