import pytest
import pytest_asyncio

from data_access.repository.cache_repository import CacheRepository

@pytest.mark.asyncio
async def test_cache_repository_set_get(cache_repository: CacheRepository, time_machine):
    key = "test_key"
    value = "test_value"

    await cache_repository.insert(key, value)
    result = await cache_repository.fetch(key)

    assert result == value

@pytest.mark.asyncio
async def test_cache_repository_delete(cache_repository: CacheRepository, time_machine):
    key = "test_key"
    value = "test_value"

    await cache_repository.insert(key, value)
    await cache_repository.delete(key)
    result = await cache_repository.fetch(key)

    assert result is None

@pytest.mark.asyncio
async def test_cache_repository_expire(cache_repository: CacheRepository, time_machine):
    key = "test_key"
    value = "test_value"
    ttl = 60

    await cache_repository.insert(key, value, ttl=ttl)

    time_machine.advance_time(ttl)

    result = await cache_repository.fetch(key)

    assert result is None

@pytest.mark.asyncio
async def test_cache_repository_set_with_dict(cache_repository: CacheRepository, time_machine):
    key = "test_key"
    value = {"field1": "value1", "field2": 2}

    await cache_repository.insert(key, value)
    result = await cache_repository.fetch(key)

    assert result == value

@pytest.mark.asyncio
async def test_cache_repository_set_without_ttl(cache_repository: CacheRepository, time_machine):
    key = "test_key"
    value = "test_value"

    await cache_repository.insert(key, value)
    result = await cache_repository.fetch(key)

    assert result == value

@pytest.mark.asyncio
async def test_cache_repository_expire_key_before_ttl(cache_repository: CacheRepository, time_machine):
    key = "test_key"
    value = "test_value"
    ttl = 60

    await cache_repository.insert(key, value, ttl=ttl)

    # Advance time by half of the TTL
    time_machine.advance_time(ttl // 2)

    result = await cache_repository.fetch(key)
    assert result == value  # The key should still exist

    time_machine.advance_time(ttl // 2)

    result = await cache_repository.fetch(key)
    assert result is None
