from fastapi import APIRouter, status, HTTPException

from ftgo_utils.logger import get_logger

from schemas.auth.account import (
    RegisterRequest, RegisterResponse,
    AuthenticateAccountRequest, AuthenticateAccountResponse,
    LoginRequest, LoginResponse,
)
from config import LayerNames, BaseConfig
from services import UserService

router = APIRouter(prefix="/account", tags=["user_profile"])
logger = get_logger(layer_name=LayerNames.GATEWAY.value, environment=BaseConfig.load_environment())

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    try:
        data = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "phone_number": request.phone_number,
            "password": request.password,
            "role": request.role,
            "national_id": request.national_id,
        }
        response = await UserService.create_profile(data)
        if response.get('status') == 'error':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=response.get('error_message', 'Unknown error occurred'))
        return RegisterResponse(user_id=response["user_id"], auth_code=response["auth_code"])
    except Exception as e:
        logger.error(f"Error occurred while registering user: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/verify", response_model=AuthenticateAccountResponse)
async def verify_account(request: AuthenticateAccountRequest):
    try:
        data = {
            "user_id": request.user_id,
            "auth_code": request.auth_code.strip(),
        }
        response = await UserService.verify_account(data)
        if response.get('status') == 'error':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get('error_message', 'Unknown error occurred'))
        return AuthenticateAccountResponse(user_id=response["user_id"])
    except Exception as e:
        logger.error(f"Error occurred while verifying the account: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        data = {
            "phone_number": request.phone_number,
            "password": request.password,
            "role": request.role,
        }
        response = await UserService.login(data)
        if response.get('status') == 'error':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get('error_message', 'Unknown error occurred'))
        
        

    except Exception as e:
        logger.error(f"Error occurred while logging the user in: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
