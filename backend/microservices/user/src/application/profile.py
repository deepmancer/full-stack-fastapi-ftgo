from typing import Dict, Any, Optional
import json
from application import get_logger
from domain import UserManager

class ProfileService:
    @staticmethod
    async def register(
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        gender: Optional[str] = None,
        email: Optional[str] = None,
        national_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        user_id, auth_code = await UserManager.register(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            role=role,
            gender=gender,
            email=email,
            national_id=national_id,
        )
        return {
            "user_id": user_id,
            "auth_code": auth_code,
        }

    @staticmethod
    async def resend_auth_code(user_id: str, **kwargs) -> Dict[str, Any]:
        auth_code = await UserManager.resend_auth_code(user_id)
        return {
            "user_id": user_id,
            "auth_code": auth_code,
        }

    @staticmethod
    async def verify_account(user_id: str, auth_code: str, **kwargs) -> Dict[str, str]:
        user = await UserManager.verify_account(user_id, auth_code.strip())
        return user.get_info()

    @staticmethod
    async def login(
        password: str,
        role: str,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, str]:
        user = await UserManager.login(
            password=password,
            role=role,
            user_id=user_id,
            phone_number=phone_number,
        )
        return user.get_info()

    @staticmethod
    async def get_info(user_id: str, **kwargs) -> Dict[str, Any]:
        user = await UserManager.load(user_id=user_id)
        return user.get_info()

    @staticmethod
    async def delete_account(user_id: str, **kwargs) -> Dict[str, str]:
        user = await UserManager.load(user_id=user_id)
        await user.delete_account()
        return {}

    @staticmethod
    async def logout(user_id: str, **kwargs) -> Dict[str, str]:
        user = await UserManager.load(user_id=user_id)
        await user.logout()
        return {}

    @staticmethod
    async def update_profile(user_id: str,
                             first_name: str,
                             last_name: str,
                             **kwargs) -> Dict[str, Any]:
        user = await UserManager.load(user_id=user_id)
        user_info = await user.update_profile_information(update_fields={
            "first_name": first_name,
            "last_name": last_name,
        })
        return user_info
