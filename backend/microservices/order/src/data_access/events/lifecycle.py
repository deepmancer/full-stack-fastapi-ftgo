import asyncio
from typing import Any

from config import BaseConfig
from data_access import get_logger
from data_access.broker import RPCBroker
from data_access.cache_repository import CacheRepository
from data_access.db_repository import DatabaseRepository


async def setup() -> None:
    logger = get_logger()
    await CacheRepository.initialize()
    get_logger().info("Connected to Redis")
    await DatabaseRepository.initialize()
    logger.info("Connected to MongoDB")
    await RPCBroker.initialize(asyncio.get_event_loop())
    logger.info("Connected to RabbitMQ")


async def teardown() -> None:
    logger = get_logger()
    await CacheRepository.terminate()
    get_logger().info("Disconnected from Redis")
    await DatabaseRepository.terminate()
    logger.info("Disconnected from MongoDB")
    await RPCBroker.terminate()
    logger.info("Disconnected from RabbitMQ")
