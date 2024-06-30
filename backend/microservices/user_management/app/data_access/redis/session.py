import redis.asyncio as redis

from configs.redis import RedisConfig

class RedisSession:
    def __init__(self, config: RedisConfig):
        self.client = None
        self.config = config

    async def initialize(self):
        self.client = redis.Redis(
            host=self.config.host,
            port=self.config.port,
            db=self.config.db,
            decode_responses=True
        )

    async def close(self):
        await self.client.close()
