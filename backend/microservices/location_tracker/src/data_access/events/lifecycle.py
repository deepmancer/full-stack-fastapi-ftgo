import asyncio
from typing import Any
from data_access.repository.hexagon import SessionRepository
from data_access.repository.location import UserRepository
from data_access.connection.db import DatabaseDataAccess
from data_access.connection.cache import CacheDataAccess
from config.db import PostgresConfig
from config.cache import RedisConfig
from data_access import get_logger

async def setup() -> None:
    db_config = PostgresConfig()
    cache_config = RedisConfig()
    DatabaseDataAccess.initialize(db_config)
    CacheDataAccess.initialize(cache_config)
    
    UserRepository.initialize(db_config)
    SessionRepository.initialize(cache_config)

    db_da = await DatabaseDataAccess.get_instance()
    cache_da = await CacheDataAccess.get_instance()

    logger = get_logger()
    await cache_da.connect()
    logger.info("Connected to Redis")
    await db_da.connect()
    logger.info("Connected to Postgres")

    unverified_users = await UserRepository.delete_unverified_users()
    await SessionRepository.delete_users_data(unverified_users)
    
    logger.info(f"Deleted unverified users with ids: {unverified_users}")

async def teardown() -> None:
    db_da = await DatabaseDataAccess.get_instance()
    cache_da = await CacheDataAccess.get_instance()

    await asyncio.gather(db_da.disconnect(), cache_da.disconnect())
