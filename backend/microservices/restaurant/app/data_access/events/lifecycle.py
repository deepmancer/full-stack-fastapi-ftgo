import asyncio
from typing import Any

from data_access.repository.cache_repository import CacheRepository
from data_access.repository.db_repository import DatabaseRepository

from data_access.resources.db import DatabaseDataAccess
from data_access.resources.cache import CacheDataAccess
from config.db import PostgresConfig
from config.cache import RedisConfig
from data_access import get_logger

async def setup() -> None:
    db_config = PostgresConfig()
    cache_config = RedisConfig()
    DatabaseDataAccess.initialize(db_config)
    CacheDataAccess.initialize(cache_config)
    
    DatabaseRepository.initialize(db_config)
    CacheRepository.initialize(cache_config)

    db_da = await DatabaseDataAccess.get_instance()
    cache_da = await CacheDataAccess.get_instance()

    logger = get_logger()
    await cache_da.connect()
    logger.info("Connected to cache")
    await db_da.connect()
    logger.info("Connected to database")

async def teardown() -> None:
    db_da = await DatabaseDataAccess.get_instance()
    cache_da = await CacheDataAccess.get_instance()

    await asyncio.gather(db_da.disconnect(), cache_da.disconnect())
