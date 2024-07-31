import asyncio
from typing import Any

from rabbitmq_rpc import RPCClient

from data_access.repository.cache_repository import CacheRepository
from data_access.repository.db_repository import DatabaseRepository
from data_access.broker import RPCBroker

from config import BaseConfig
from data_access import get_logger

async def setup() -> None:
    logger = get_logger()
    await CacheRepository.initialize()
    logger.info("Connected to Redis")
    await DatabaseRepository.initialize()
    logger.info("Connected to PostgreSQL")
    await RPCBroker.initialize(asyncio.get_event_loop())
    logger.info("Connected to RabbitMQ")


async def teardown() -> None:
    logger = get_logger()
    await CacheRepository.terminate()
    logger.info("Disconnected from Redis")
    await DatabaseRepository.terminate()
    logger.info("Disconnected from PostgreSQL")
    await RPCBroker.terminate()
    logger.info("Disconnected from RabbitMQ")