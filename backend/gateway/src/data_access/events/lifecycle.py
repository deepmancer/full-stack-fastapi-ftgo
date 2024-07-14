import asyncio
from typing import Any


from data_access.resources.cache import CacheDataAccess
from config.cache import RedisConfig
from data_access import get_logger

async def setup() -> None:
    cache_config = RedisConfig()
    CacheDataAccess.initialize(cache_config)
    cache_da = await CacheDataAccess.get_instance()

    logger = get_logger()
    await cache_da.connect()
    logger.info("Connected to cache")
    
async def teardown() -> None:
    cache_da = await CacheDataAccess.get_instance()

    await cache_da.disconnect()
