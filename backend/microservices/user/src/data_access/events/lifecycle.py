import asyncio
from typing import Any

from data_access.repository.cache_repository import CacheRepository
from data_access.repository.db_repository import DatabaseRepository

from config.db import PostgresConfig
from config.cache import RedisConfig
from data_access import get_logger

async def setup() -> None:
    db_config = PostgresConfig()
    cache_config = RedisConfig()
    logger = get_logger()
    await CacheRepository.initialize(cache_config)
    logger.info("Connected to cache")
    await DatabaseRepository.initialize(db_config)
    logger.info("Connected to database")

async def teardown() -> None:
    logger = get_logger()
    await CacheRepository.terminate()
    logger.info("Disconnected from cache")
    await DatabaseRepository.terminate()
    logger.info("Disconnected from database")
