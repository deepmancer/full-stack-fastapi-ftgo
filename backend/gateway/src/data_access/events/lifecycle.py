import asyncio
from typing import Any

from rabbitmq_rpc import RPCClient

from data_access.repository.cache_repository import CacheRepository
from data_access.broker import RPCBroker

from config import BaseConfig
from data_access import get_logger
RPCClient
async def setup() -> None:
    logger = get_logger()
    await CacheRepository.initialize()
    logger.info("Connected to Redis")
    await RPCBroker.initialize()
    logger.info("Connected to RabbitMQ")


async def teardown() -> None:
    logger = get_logger()
    await CacheRepository.terminate()
    logger.info("Disconnected from Redis")
    await RPCBroker.terminate()
    logger.info("Disconnected from RabbitMQ")