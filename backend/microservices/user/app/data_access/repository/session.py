from typing import Optional
from data_access.connection.cache import CacheDataAccess
from config.cache import RedisConfig

class SessionRepository:
    AUTH_CODE_PREFIX = "auth_"
    SESSION_TOKEN_PREFIX = "token_"

    data_access: Optional[CacheDataAccess] = None

    @classmethod
    def initialize(cls, cache_config: RedisConfig):
        cls.data_access = CacheDataAccess(cache_config)

    @classmethod
    def create_auth_key(cls, key: str) -> str:
        return f"{cls.AUTH_CODE_PREFIX}{key}"

    @classmethod
    def create_token_key(cls, key: str) -> str:
        return f"{cls.SESSION_TOKEN_PREFIX}{key}"
  
    @classmethod
    async def cache_auth_code(cls, user_id: str, auth_code: str, ttl: int):
        key = cls.create_auth_key(user_id)
        await cls.data_access.set(key, auth_code, ttl)

    @classmethod
    async def cache_token(cls, user_id: str, token: str, ttl: int):
        key = cls.create_token_key(user_id)
        await cls.data_access.set(key, token, ttl)

    @classmethod
    async def get_auth_code_by_user_id(cls, user_id: str) -> Optional[str]:
        key = cls.create_auth_key(user_id)
        auth_code = await cls.data_access.get(key)
        return auth_code

    @classmethod
    async def get_token_by_user_id(cls, user_id: str) -> Optional[str]:
        key = cls.create_token_key(user_id)
        token = await cls.data_access.get(key)
        return token

    @classmethod
    async def delete_user_auth_code(cls, user_id: str):
        key = cls.create_auth_key(user_id)
        await cls.data_access.delete(key)

    @classmethod
    async def delete_user_token(cls, user_id: str):
        key = cls.create_token_key(user_id)
        await cls.data_access.delete(key)

    @classmethod
    async def flush_user_cached_data(cls, user_id: str):
        auth_key = cls.create_auth_key(user_id)
        token_key = cls.create_token_key(user_id)
        async with cls.data_access.pipeline() as pipe:
            pipe.delete(auth_key)
            pipe.delete(token_key)
            await pipe.execute()
