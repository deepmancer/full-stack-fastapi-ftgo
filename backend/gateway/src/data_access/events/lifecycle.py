import asyncio
from typing import Any

from data_access.repository.cache_repository import CacheRepository

from config.cache import RedisConfig
from data_access import get_logger

async def setup() -> None:
    cache_config = RedisConfig.load()
    logger = get_logger()
    await CacheRepository.initialize(cache_config)
    logger.info("Connected to cache")

async def teardown() -> None:
    logger = get_logger()
    await CacheRepository.terminate()
    logger.info("Disconnected from cache")
