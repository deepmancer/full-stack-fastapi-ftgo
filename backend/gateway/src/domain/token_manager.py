from datetime import timedelta
from typing import Optional

from application.schemas.user import UserStateSchema
from config import AuthConfig
from data_access.repository import CacheRepository
from domain import get_logger
from ftgo_utils.errors import ErrorCodes
from ftgo_utils.jwt_auth import encode
from utils.exception import handle_exception


class TokenManager:
    def __init__(self, auth_config: Optional[AuthConfig] = None):
        self.auth_config = auth_config if auth_config else self.get_config()
        self.cache = CacheRepository.get_cache(self.auth_config.cache_key_prefix)

    @classmethod
    def get_config(cls):
        return AuthConfig()

    async def generate_token(
        self,
        user_id: str,
        phone_number: str,
        role: str,
        hashed_password: str,
    ) -> str:
        payload = {
            "user_id": user_id,
            "phone_number": phone_number,
            "role": role,
            "hashed_password": hashed_password,
        }
        access_token_expires = timedelta(minutes=self.auth_config.access_token_expire_minutes)
        token = encode(
            payload=payload,
            secret=self.auth_config.secret,
            algorithm=self.auth_config.algorithm,
            expiration=access_token_expires.total_seconds()
        )

        await self.cache.set(
            key=token,
            value=payload,
            ttl=int(access_token_expires.total_seconds()),
        )
        get_logger().info(f"Generated a session token for user_id {user_id}")
        return token

    async def invalidate_token(
        self,
        token: str,
    ) -> None:
        await self.cache.delete(token)
        get_logger().info("Deleted the session token")

    async def fetch_user(
        self,
        token: str,
    ) -> Optional[UserStateSchema]:
        try:
            payload = await self.cache.get(token)
            if not payload:
                return None
            return UserStateSchema.model_validate({
                "token": token,
                **payload,
            })
        except Exception as e:
            payload = {"token": token}
            get_logger().error(ErrorCodes.TOKEN_NOT_FOUND_ERROR.value)
            await handle_exception(e, error_code=ErrorCodes.TOKEN_NOT_FOUND_ERROR, payload=payload)
