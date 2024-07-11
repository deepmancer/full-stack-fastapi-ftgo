import contextlib
from typing import Optional

import redis.asyncio as redis

from config.cache import RedisConfig
from data_access.exceptions import CacheConnectionError, CacheSessionCreationError
from data_access.resources.base import BaseDataAccess


class CacheDataAccess(BaseDataAccess):
    _config: Optional[RedisConfig] = None

    def __init__(self, config: RedisConfig):
        self.initialize(config)
        self.session = None

    @contextlib.asynccontextmanager
    async def get_or_create_session(self) -> redis.Redis:
        try:
            if self.session is None:
                await self.connect()
            yield self.session
        except Exception as e:
            self.logger.error(f"Failed to create session for Redis at {self._config.url}")
            raise CacheSessionCreationError() from e

    async def connect(self) -> None:
        try:
            self.logger.info(f"Connecting to Redis at {self._config.url}")
            self.session = redis.Redis.from_url(self._config.url, decode_responses=True)
            await self.session.ping()
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis at {self._config.url}")
            raise CacheConnectionError(self._config.url) from e
            
    async def disconnect(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None
