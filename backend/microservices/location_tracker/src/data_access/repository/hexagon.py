from typing import Optional, List
from data_access.connection.cache import CacheDataAccess
from config.cache import RedisConfig

class SessionRepository:
    data_access: Optional[CacheDataAccess] = None

    @classmethod
    def initialize(cls, cache_config: RedisConfig):
        cls._data_access = CacheDataAccess(cache_config)

    @classmethod
    async def cache_(cls, hexa: str, auth_code: str, ttl: int):
        key = cls.create_auth_key(user_id)
        await cls._data_access.set(key, auth_code, ttl)

    @classmethod
    async def cache_token(cls, user_id: str, token: str, ttl: int):
        key = cls.create_token_key(user_id)
        await cls._data_access.set(key, token, ttl)

    @classmethod
    async def get_auth_code_by_user_id(cls, user_id: str) -> Optional[str]:
        key = cls.create_auth_key(user_id)
        auth_code = await cls._data_access.get(key)
        return auth_code

    @classmethod
    async def get_token_by_user_id(cls, user_id: str) -> Optional[str]:
        key = cls.create_token_key(user_id)
        token = await cls._data_access.get(key)
        return token

    @classmethod
    async def delete_user_auth_code(cls, user_id: str):
        key = cls.create_auth_key(user_id)
        await cls._data_access.delete(key)

    @classmethod
    async def delete_user_token(cls, user_id: str):
        key = cls.create_token_key(user_id)
        await cls._data_access.delete(key)

    @classmethod
    async def delete_user_data(cls, user_id: str):
        auth_key = cls.create_auth_key(user_id)
        token_key = cls.create_token_key(user_id)
        pipeline = await cls._data_access.pipeline()
        pipeline.delete(auth_key)
        pipeline.delete(token_key)
        await pipeline.execute()

    @classmethod
    async def delete_users_data(cls, user_ids: List[str]):
        pipe = await cls._data_access.pipeline()
        for user_id in user_ids:
            auth_key = cls.create_auth_key(user_id)
            token_key = cls.create_token_key(user_id)
            pipe.delete(auth_key)
            pipe.delete(token_key)
        await pipe.execute()
