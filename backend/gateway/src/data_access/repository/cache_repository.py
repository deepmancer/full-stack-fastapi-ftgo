import json
from typing import List, Optional, Union

from aredis_client import AsyncRedis
from ftgo_utils.errors import ErrorCodes

from config import RedisConfig
from data_access import get_logger
from utils import handle_exception

class CacheRepository():
    _data_access: Optional[AsyncRedis] = None
    _group: str = ""

    @classmethod
    async def initialize(cls):
        cache_config = RedisConfig()
        try:
            cls._data_access = await AsyncRedis.create(
                host=cache_config.host,
                port=cache_config.port,
                db=cache_config.db,
                password=cache_config.password,
            )
        except Exception as e:
            payload = cache_config.dict()
            get_logger().error(ErrorCodes.CACHE_CONNECTION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_CONNECTION_ERROR, payload=payload)

    @classmethod
    def get_cache(cls, group: str = ""):
        cls._group = group
        return cls

    @classmethod
    def _prefixed_key(cls, key: str) -> str:
        return f"{cls._group}:{key}"

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
            payload = dict(key=key)
            get_logger().error(ErrorCodes.CACHE_FETCH_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_FETCH_ERROR, payload=payload)

    @classmethod
    async def set(cls, key: str, value: Union[str, dict], ttl: Optional[int] = None) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                serialized_value = cls._serialize_value(value)
                await session.set(cls._prefixed_key(key), serialized_value, ex=ttl)
        except Exception as e:
            payload = dict(key=key, value=value, ttl=ttl)
            get_logger().error(ErrorCodes.CACHE_INSERT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_INSERT_ERROR, payload=payload)

    @classmethod
    async def delete(cls, key: str) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.delete(cls._prefixed_key(key))
        except Exception as e:
            payload = dict(key=key)
            get_logger().error(ErrorCodes.CACHE_DELETE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_DELETE_ERROR, payload=payload)

    @classmethod
    async def expire(cls, key: str, ttl: int) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.expire(cls._prefixed_key(key), ttl)
        except Exception as e:
            payload = dict(key=key, ttl=ttl)
            get_logger().error(ErrorCodes.CACHE_EXPIRE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_EXPIRE_ERROR, payload=payload)

    @classmethod
    async def batch_delete(cls, keys: List[str]) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                pipeline = session.pipeline()
                for key in keys:
                    pipeline.delete(cls._prefixed_key(key))
                await pipeline.execute()
        except Exception as e:
            payload = dict(keys=keys)
            get_logger().error(ErrorCodes.CACHE_DELETE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_DELETE_ERROR, payload=payload)

    @classmethod
    async def flush(cls) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.flushdb()
        except Exception as e:
            get_logger().error(ErrorCodes.CACHE_FLUSH_ERROR.value)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_FLUSH_ERROR)

    @classmethod
    async def terminate(cls) -> None:
        if cls._data_access:
            await cls._data_access.disconnect()
            cls._data_access = None
