import redis.asyncio as redis
import asyncio
from typing import Optional
from configs.cache import RedisConfig
from data_access.session.base import BaseDataAccess
class CacheDataAccess(BaseDataAccess):
    _config: Optional[RedisConfig] = None

    def __init__(self, config: RedisConfig):
        super().initialize(config)
        self.session: Optional[redis.Redis] = None

    async def get_or_create_session(self) -> redis.Redis:
        if self.session is None:
            await self.connect()
        return self.session

    async def connect(self) -> None:
        self.session = redis.Redis.from_url(self._config.url, decode_responses=True)
        await self.session.ping()

    async def disconnect(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None