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

    async def get(self, key: str) -> str:
        session = await self.get_or_create_session()
        return await session.get(key)

    async def set(self, key: str, value: str, ttl=None) -> None:
        session = await self.get_or_create_session()
        await session.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        session = await self.get_or_create_session()
        await session.delete(key)

    async def expire(self, key: str, ttl: int) -> None:
        session = await self.get_or_create_session()
        await session.expire(key, ttl)

    async def pipeline(self):
        session = await self.get_or_create_session()
        return session.pipeline()
