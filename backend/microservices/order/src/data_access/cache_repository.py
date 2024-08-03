import json
from typing import List, Optional, Union

from aredis_client import AsyncRedis
from ftgo_utils.errors import ErrorCodes

from config import RedisConfig
from data_access import get_logger
from data_access.base import BaseRepository
from utils import handle_exception

class CacheRepository(BaseRepository):
    _data_access: Optional[AsyncRedis] = None
    _group: str = ""

    @classmethod
    async def initialize(cls) -> None:
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
    async def fetch(
        cls,
        keys: Union[List[str], str],
        data_type: str = "string",
        fields: Union[List[str], str] = None
    ) -> Union[str, dict, None, List[Union[str, dict, None]]]:
        try:
            single_fetch = isinstance(keys, str)
            to_fetch_keys = [keys] if single_fetch else keys
            to_fetch_fields = [fields] if isinstance(fields, str) else fields
            
            async with cls._data_access.get_or_create_session() as session:
                pipeline = session.pipeline()
                
                if data_type == "hash":
                    if to_fetch_fields:  # Fetch specific fields
                        for key, field in zip(to_fetch_keys, to_fetch_fields):
                            pipeline.hget(cls._prefixed_key(key), field)
                    else:  # Fetch entire hash
                        for key in to_fetch_keys:
                            pipeline.hgetall(cls._prefixed_key(key))
                elif data_type == "list":
                    for key in to_fetch_keys:
                        pipeline.lrange(cls._prefixed_key(key), 0, -1)
                else:  # Default to string
                    for key in to_fetch_keys:
                        pipeline.get(cls._prefixed_key(key))
                
                values = await pipeline.execute()
                
                if data_type == "hash":
                    deserialized_values = []
                    for value_dict in values:
                        if value_dict:
                            deserialized_dict = {key: cls._deserialize_value(value) if value else None for key, value in value_dict.items()}
                            deserialized_values.append(deserialized_dict)
                        else:
                            deserialized_values.append(None)
                else:
                    deserialized_values = [
                        cls._deserialize_value(value) if value else None
                        for value in values
                    ]
                
                return deserialized_values[0] if single_fetch else deserialized_values
            
        except Exception as e:
            payload = {"keys": keys, "fields": fields}
            get_logger().error(ErrorCodes.CACHE_FETCH_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_FETCH_ERROR, payload=payload)

    @classmethod
    async def update(
        cls,
        keys: Union[str, List[str]],
        values: Union[str, dict, List[Union[str, dict]]],
        ttl: Optional[int] = None,
    ) -> None:
        await cls.insert(keys, values, ttl)

    @classmethod
    async def insert(
        cls,
        keys: Union[str, List[str]],
        values: Union[str, dict, List[Union[str, dict]]],
        ttl: Optional[int] = None,
        data_type: str = "string"
    ) -> None:
        to_insert_keys = [keys] if isinstance(keys, str) else keys
        to_insert_values = [values] if not isinstance(values, list) else values
        if len(to_insert_keys) != len(to_insert_values):
            raise ValueError("Keys and values must have the same length")
        try:
            async with cls._data_access.get_or_create_session() as session:
                pipeline = session.pipeline()
                for key, value in zip(to_insert_keys, to_insert_values):
                    if data_type == "hash" and isinstance(value, dict):
                        for field, val in value.items():
                            pipeline.hset(cls._prefixed_key(key), field, cls._serialize_value(val))
                    elif data_type == "list" and isinstance(value, list):
                        for item in value:
                            pipeline.rpush(cls._prefixed_key(key), cls._serialize_value(item))
                    else:
                        pipeline.set(cls._prefixed_key(key), cls._serialize_value(value), ex=ttl)
                await pipeline.execute()
        except Exception as e:
            payload = {"keys": keys, "values": values, "ttl": ttl}
            get_logger().error(ErrorCodes.CACHE_INSERT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_INSERT_ERROR, payload=payload)

    @classmethod
    async def delete(
        cls,
        keys: Union[List[str], str],
        data_type: str = "string",
        fields: Optional[Union[str, List[str]]] = None
    ) -> None:
        try:
            to_delete_keys = [keys] if isinstance(keys, str) else keys
            async with cls._data_access.get_or_create_session() as session:
                pipeline = session.pipeline()
                if data_type == "hash" and fields:
                    for key in to_delete_keys:
                        if isinstance(fields, str):
                            fields_to_delete = [fields]
                        else:
                            fields_to_delete = fields
                        pipeline.hdel(cls._prefixed_key(key), *fields_to_delete)
                else:
                    for key in to_delete_keys:
                        pipeline.delete(cls._prefixed_key(key))
                await pipeline.execute()
        except Exception as e:
            payload = {"keys": keys, "fields": fields}
            get_logger().error(ErrorCodes.CACHE_DELETE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_DELETE_ERROR, payload=payload)


    @classmethod
    async def expire(cls, keys: Union[str, List[str]], ttl: int) -> None:
        to_expire_keys = [keys] if isinstance(keys, str) else keys
        try:
            async with cls._data_access.get_or_create_session() as session:
                pipeline = session.pipeline()
                for key in to_expire_keys:
                    pipeline.expire(cls._prefixed_key(key), ttl)
                await pipeline.execute()
        except Exception as e:
            payload = {"keys": keys, "ttl": ttl}
            get_logger().error(ErrorCodes.CACHE_EXPIRE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.CACHE_EXPIRE_ERROR, payload=payload)

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

    @classmethod
    def _prefixed_key(cls, key: str) -> str:
        return f"{cls._group}:{key}"

    @classmethod
    def _serialize_value(cls, value: Union[str, dict]) -> str:
        return json.dumps(value) if isinstance(value, dict) else value

    @classmethod
    def _deserialize_value(cls, value: str) -> Union[str, dict]:
        try:
            return json.loads(value)
        except Exception as e:
            return value

    @classmethod
    def get_cache(cls, group: str = "") -> "CacheRepository":
        cls._group = group
        return cls
