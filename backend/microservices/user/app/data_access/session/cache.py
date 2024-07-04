import redis.asyncio as redis
from data_access.session.interface import AsyncSessionInterface
from configs.cache import RedisConfig

class CacheSession(AsyncSessionInterface):
    def __init__(self, config: RedisConfig):
        self.config = config
        self.session = None

    async def get_or_create_session(self):
        if self.session is None:
            await self.connect()
        return self.session
    
    async def connect(self):
        self.session = redis.Redis.from_url(self.config.redis_url, decode_responses=True)
        await self.session.ping()

    async def disconnect(self):
        if self.session:
            await self.session.close()
            self.session = None
