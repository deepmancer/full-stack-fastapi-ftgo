from typing import Dict, Any, Optional
import json
from application import get_logger
from domain.user import UserDomain

class ProfileService:
    @staticmethod
    async def register(
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        email: Optional[str] = None,
        national_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        user_id, auth_code = await UserDomain.register(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            role=role,
            email=email,
            national_id=national_id,
        )
        return {
            "user_id": user_id,
            "auth_code": auth_code,
        }

    @staticmethod
    async def resend_auth_code(user_id: str) -> Dict[str, Any]:
        auth_code = await UserDomain.resend_auth_code(user_id)
        return {
            "user_id": user_id,
            "auth_code": auth_code,
        }

    @staticmethod
    async def verify_account(user_id: str, auth_code: str) -> Dict[str, str]:
        user = await UserDomain.verify_account(user_id, auth_code.strip())
        return user.get_info()

    @staticmethod
    async def login(
        password: str,
        role: str,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> Dict[str, str]:
        user = await UserDomain.login(password, role, user_id, phone_number)
        return user.get_info()

    @staticmethod
    async def get_info(user_id: str) -> Dict[str, Any]:
        user = await UserDomain.load(user_id=user_id)
        return await user.get_info()

    @staticmethod
    async def delete_account(user_id: str) -> Dict[str, str]:
        user = await UserDomain.load(user_id=user_id)
        await user.delete_account()
        return {}

    @staticmethod
    async def logout(user_id: str) -> Dict[str, str]:
        user = await UserDomain.load(user_id=user_id)
        await user.logout()
        return {}

    @staticmethod
    async def update_profile(user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        user = await UserDomain.load(user_id=user_id)
        await user.update_profile_information(update_data)
        return user.get_info()
