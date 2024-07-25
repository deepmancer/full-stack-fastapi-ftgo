import json
from typing import List, Optional, Union

from aredis_client import AsyncRedis

from config.cache import RedisConfig
from data_access.exceptions import *

class CacheRepository:
    _data_access: Optional[AsyncRedis] = None
    _group: str = ""

    @classmethod
    async def initialize(cls):
        cache_config = RedisConfig()
        cls._data_access = await AsyncRedis.create(
            host=cache_config.host,
            port=cache_config.port,
            db=cache_config.db,
            password=cache_config.password,
        )

    @classmethod
    def get_cache(cls, group: str = ""): 
        cls._group = group
        return cls

    @classmethod
    def _prefixed_key(cls, key: str) -> str:
        return f"{cls._group}{key}"

    @classmethod
    def _serialize_value(cls, value: Union[str, dict]) -> str:
        if isinstance(value, dict):
            return json.dumps(value)
        return value

    @classmethod
    def _deserialize_value(cls, value: str) -> Union[str, dict]:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    @classmethod
    async def get(cls, key: str) -> Union[str, dict, None]:
        try:
            async with cls._data_access.get_or_create_session() as session:
                value = await session.get(cls._prefixed_key(key))
                if value:
                    return cls._deserialize_value(value)
                return None
        except Exception as e:
            raise CacheFetchError(key, message=str(e))

    @classmethod
    async def set(cls, key: str, value: Union[str, dict], ttl=None) -> None:
        try:
            print('hello')
            async with cls._data_access.get_or_create_session() as session:
                print('how are your')
                serialized_value = cls._serialize_value(value)
                print('fuck you')
                print(serialized_value)
                print()
                print(type(serialized_value))
                print()
                print(cls._prefixed_key(key))
                print(ttl)
                print(type(ttl))
                print('-------------')
                await session.set(cls._prefixed_key(key), serialized_value, ex=ttl)
        except Exception as e:
            print(e)
            raise CacheInsertError(key=key, value=value, message=str(e))

    @classmethod
    async def delete(cls, key: str) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.delete(cls._prefixed_key(key))
        except Exception as e:
            raise CacheDeleteError(key, message=str(e))

    @classmethod
    async def expire(cls, key: str, ttl: int) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.expire(cls._prefixed_key(key), ttl)
        except Exception as e:
            raise CacheExpireError(key, ttl, message=str(e))

    @classmethod
    async def batch_delete(cls, keys: List[str]):
        try:
            async with cls._data_access.get_or_create_session() as session:
                pipeline = session.pipeline()
                for key in keys:
                    pipeline.delete(cls._prefixed_key(key))
                await pipeline.execute()
        except Exception as e:
            raise CacheBatchOperationError(metadata={"keys": keys}, message=str(e))

    @classmethod
    async def flush(cls):
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.flushdb()
        except Exception as e:
            raise CacheFlushError(message=str(e))

    @classmethod
    async def terminate(cls):
        await cls._data_access.disconnect()