import asyncio
from typing import Any
from data_access.repository import UserRepository
from data_access.connection.db import DatabaseDataAccess
from data_access.connection.cache import CacheDataAccess
from config.db import PostgresConfig
from config.cache import RedisConfig

async def setup() -> None:
    from loguru import logger
    db_config = PostgresConfig()
    cache_config = RedisConfig()
    DatabaseDataAccess.initialize(db_config)
    CacheDataAccess.initialize(cache_config)
    
    UserRepository.initialize(db_config, cache_config)

    db_da = await DatabaseDataAccess.get_instance()
    cache_da = await CacheDataAccess.get_instance()

    await cache_da.connect()
    logger.info("Connected to cache")
    await db_da.connect()
    logger.info("Connected to database")
    

async def teardown() -> None:
    db_da = await DatabaseDataAccess.get_instance()
    cache_da = await CacheDataAccess.get_instance()

    await asyncio.gather(db_da.disconnect(), cache_da.disconnect())
