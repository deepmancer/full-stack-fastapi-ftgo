from typing import Dict

from application.interfaces.profile import *
from domain.user import UserDomain
from ftgo_utils.logger import get_logger
class ProfileService:

    @staticmethod
    async def register(
        *,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        national_id: str = None,
        ) -> Dict:
        try:
            user_id, auth_code = await UserDomain.register(
                first_name=request.first_name,
                last_name=request.last_name,
                phone_number=request.phone_number,
                password=request.password,
                role=request.role,
                national_id=request.national_id,
            )
            return {
                "status": "success",
                "user_id": user_id,
                "auth_code": auth_code,
            }
        except Exception as e:
            get_logger().error(f"Error in registering user: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }

    @staticmethod
    async def verify_account(request: AuthenticateAccountRequest) -> AuthenticateAccountResponse:
        user_id = await UserDomain.verify_account(request.user_id, request.auth_code.strip())
        return AuthenticateAccountResponse(user_id=user_id, success=True)

    @staticmethod
    async def login(request: LoginRequest) -> LoginResponse:
        user = await UserDomain.load(phone_number=request.phone_number, role=request.role)
        await user.login(request.password)
        return LoginResponse(user_id=user.user_id, success=True)

    @staticmethod
    async def get_info(request: GetUserInfoRequest) -> GetUserInfoResponse:
        user = await UserDomain.load(request.user_id)
        user_info = user.get_info()
        return GetUserInfoResponse(
            user_id=user_info["user_id"],
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            phone_number=user_info["phone_number"],
            gender=user_info["gender"],
            role=user_info["role"],
        )

    @staticmethod
    async def delete_account(request: DeleteProfileRequest) -> DeleteProfileResponse:
        user = await UserDomain.load(request.user_id)
        await user.delete_account()
        return DeleteProfileResponse(user_id=user.user_id, success=True)

    @staticmethod
    async def logout(request: LogoutRequest) -> LogoutResponse:
        user = await UserDomain.load(request.user_id)
        await user.logout()
        return LogoutResponse(user_id=user.user_id, success=True)

    @staticmethod
    async def update_profile(request: UpdateProfileRequest) -> UpdateProfileResponse:
        user = await UserDomain.load(request.user_id)
        user_info = await user.update_profile_information(request.dict(exclude={"user_id"}))
        return UpdateProfileResponse(success=True, **user_info)

    @staticmethod
    async def get_user_info_with_credentials(request: GetUserWithCredentialsRequest) -> GetUserWithCredentialsResponse:
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
