import asyncio
from typing import Any

from data_access.repository.cache_repository import CacheRepository

from config.base import BaseConfig
from data_access import get_logger

async def setup() -> None:
    BaseConfig()
    logger = get_logger()
    await CacheRepository.initialize()
    logger.info("Connected to Redis")

async def teardown() -> None:
    logger = get_logger()
    await CacheRepository.terminate()
    logger.info("Disconnected from cache")
