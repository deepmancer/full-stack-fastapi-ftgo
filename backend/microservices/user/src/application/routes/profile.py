import os
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application import get_logger
from backend.microservices.user.src.application.routes_schema import *
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
        get_logger().error(f"Error occurred while registering user: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/verify", response_model=AuthenticateAccountResponse)
async def verify_account(request: AuthenticateAccountRequest):
    try:
        user_id = await UserDomain.verify_account(request.user_id, request.auth_code.strip())
        return AuthenticateAccountResponse(user_id=user_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while verifying the account: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        user = await UserDomain.load(phone_number=request.phone_number, role=request.role)
        await user.login(request.password)
        return LoginResponse(user_id=user.user_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while logging the user in: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

# logout api
@router.get("/user_info", response_model=GetUserInfoResponse)
async def get_info(request: GetUserInfoRequest):
    try:
        user = await UserDomain.load(request.user_id)
        user_info = user.get_info()
        return GetUserInfoResponse(
            user_id=user_info["user_id"],
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            phone_number=user_info["phone_number"],
            hashed_password=user_info["hashed_password"],
            gender=user_info["gender"],
            role=user_info["role"],
        )
    except Exception as e:
        get_logger().error(f"Error occurred while getting the user info: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))

@router.delete("/delete", response_model=DeleteProfileResponse)
async def delete_account(request: DeleteProfileRequest):
    try:
        user = await UserDomain.load(request.user_id)
        await user.delete_account()
        return DeleteProfileResponse(user_id=user.user_id, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while deleting the account: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))


# a post api for updating user profile fields
@router.post("/update", response_model=UpdateProfileResponse)
async def update_profile(request: UpdateProfileRequest):
    try:
        user = await UserDomain.load(request.user_id)
        updated_fields = await user.update_profile_information(request.updated_fields)
        return UpdateProfileResponse(user_id=user.user_id, updated_fields=updated_fields, success=True)
    except Exception as e:
        get_logger().error(f"Error occurred while updating the user profile: {e}", request=request)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": str(e)}))