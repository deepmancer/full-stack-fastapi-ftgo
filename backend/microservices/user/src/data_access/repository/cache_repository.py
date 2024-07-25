import json
from typing import List, Optional, Union

from aredis_client import AsyncRedis
from ftgo_utils.errors import ErrorCodes

from config import RedisConfig, DataAccessError
from data_access import get_logger, layer_name
from data_access.repository.base import BaseRepository
from utils.error_handler import handle_error

class CacheRepository(BaseRepository):
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
            get_logger().error(f"Error connecting to cache: config={cache_config}, error={e}")
            return handle_error(e=e, error_code=ErrorCodes.CACHE_CONNECTION_ERROR, layer=layer_name)

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
            get_logger().error(f"Error fetching cache: key={key}, error={e}")
            return handle_error(e=e, error_codee=ErrorCodes.CACHE_FETCH_ERROR, layer=layer_name)

    @classmethod
    async def set(cls, key: str, value: Union[str, dict], ttl: Optional[int] = None) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                serialized_value = cls._serialize_value(value)
                await session.set(cls._prefixed_key(key), serialized_value, ex=ttl)
        except Exception as e:
            get_logger().error(f"Error setting cache: key={key}, value={value}, ttl={ttl}, error={e}")
            return handle_error(e=e, error_codee=ErrorCodes.CACHE_INSERT_ERROR, layer=layer_name)

    @classmethod
    async def delete(cls, key: str) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.delete(cls._prefixed_key(key))
        except Exception as e:
            get_logger().error(f"Error deleting cache: key={key}, error={e}")
            return handle_error(e=e, error_codee=ErrorCodes.CACHE_DELETE_ERROR, layer=layer_name)

    @classmethod
    async def expire(cls, key: str, ttl: int) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.expire(cls._prefixed_key(key), ttl)
        except Exception as e:
            get_logger().error(f"Error expiring cache: key={key}, ttl={ttl}, exception={e}")
            return handle_error(e=e, error_codee=ErrorCodes.CACHE_EXPIRE_ERROR, layer=layer_name)

    @classmethod
    async def batch_delete(cls, keys: List[str]) -> None:
        if cls._data_access is None:
            raise DataAccessError(error_code=ErrorCodes.CACHE_NOT_INITIALIZED)
        try:
            async with cls._data_access.get_or_create_session() as session:
                pipeline = session.pipeline()
                for key in keys:
                    pipeline.delete(cls._prefixed_key(key))
                await pipeline.execute()
        except Exception as e:
            get_logger().error(f"Error batch deleting cache: keys={key}, error={e}")
            return handle_error(e=e, error_codee=ErrorCodes.CACHE_DELETE_ERROR, layer=layer_name)

    @classmethod
    async def flush(cls) -> None:
        try:
            async with cls._data_access.get_or_create_session() as session:
                await session.flushdb()
        except Exception as e:
            get_logger().error(f"Error flushing cache: {e}")
            return handle_error(e=e, error_codee=ErrorCodes.CACHE_FLUSH_ERROR, layer=layer_name)

    @classmethod
    async def terminate(cls) -> None:
        if cls._data_access:
            await cls._data_access.disconnect()
            cls._data_access = None
