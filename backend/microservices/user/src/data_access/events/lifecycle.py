import asyncio
from typing import Any

from data_access.repository.cache_repository import CacheRepository
from data_access.repository.db_repository import DatabaseRepository

from models import Base, Address, VehicleInfo, Profile
from config.db import PostgresConfig
from config.cache import RedisConfig
from data_access import get_logger

async def setup() -> None:
    db_config = PostgresConfig.load()
    cache_config = RedisConfig.load()
    logger = get_logger()
    await CacheRepository.initialize(cache_config)
    logger.info("Connected to cache")
    await DatabaseRepository.initialize(db_config)
    logger.info("Connected to database")
    async with DatabaseRepository.data_access._async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    logger.info("Tables created")
async def teardown() -> None:
    logger = get_logger()
    await CacheRepository.terminate()
    logger.info("Disconnected from cache")
    await DatabaseRepository.terminate()
    logger.info("Disconnected from database")
