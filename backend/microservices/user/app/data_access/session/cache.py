import redis.asyncio as redis
from loguru import logger
from typing import Optional
from config.cache import RedisConfig
from data_access.session.base import BaseDataAccess

class CacheDataAccess(BaseDataAccess):
    _config: Optional[RedisConfig] = None

    def __init__(self, config: RedisConfig):
        self.initialize(config)
        self.session = None

    async def get_or_create_session(self) -> redis.Redis:
        if self.session is None:
            await self.connect()
        return self.session

    async def connect(self) -> None:
        logger.debug(f"Connecting to Redis at {self._config.url}")
        self.session = redis.Redis.from_url(self._config.url, decode_responses=True)
        await self.session.ping()
        

    async def disconnect(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None

    @classmethod
    async def get(cls, key: str) -> str:
        session = await cls.get_or_create_session()
        return await session.get(key)

    @classmethod
    async def set(cls, key: str, value: str, ttl=None) -> None:
        session = await cls.get_or_create_session()
        await session.set(key, value, ex=ttl)

    @classmethod
    async def delete(cls, key: str) -> None:
        session = await cls.get_or_create_session()
        await session.delete(key)

    @classmethod
    async def expire(cls, key: str, ttl: int) -> None:
        session = await cls.get_or_create_session()
        await session.expire(key, ttl)

    @classmethod
    async def pipeline(cls):
        session = await cls.get_or_create_session()
        return session.pipeline()
