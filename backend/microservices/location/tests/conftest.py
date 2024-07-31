import pytest
import asyncio
import pytest_asyncio

from test_doubles.redis import FakeAsyncRedis
from test_doubles.time import TimeProvider
from data_access.repository.cache_repository import CacheRepository

MOCKED_TIMESTAMP = 1704067200 # 2024, January 1	

@pytest.fixture(scope='function')
def time_machine():
    provider = TimeProvider(timestamp=MOCKED_TIMESTAMP)
    provider.start()
    yield provider
    provider.stop()

@pytest_asyncio.fixture(scope='function')
async def fake_redis(time_machine: TimeProvider):
    redis = await FakeAsyncRedis.create(
        host="localhost", 
        port=6379, 
        db=0, 
        time_provider=time_machine.current_timestamp
    )
    return redis

@pytest_asyncio.fixture(scope='function')
async def cache_repository(fake_redis):
    CacheRepository._data_access = fake_redis
    yield CacheRepository

@pytest_asyncio.fixture
async def setup_and_teardown_cache(cache_repository):
    """Setup and teardown for each test using CacheRepository."""
    async with cache_repository._data_access.get_or_create_session() as session:
        await session.flushdb()
    yield
    async with cache_repository._data_access.get_or_create_session() as session:
        await session.flushdb()
