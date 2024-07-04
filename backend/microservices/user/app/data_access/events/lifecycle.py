import asyncio
from typing import Any
from data_access.session.db import DatabaseDataAccess
from data_access.session.cache import CacheDataAccess
from configs.db import PostgresConfig
from configs.cache import RedisConfig

async def setup(db_config: PostgresConfig, cache_config: RedisConfig) -> None:
    db_da = DatabaseDataAccess.initialize(db_config)
    cache_da = CacheDataAccess.initialize(cache_config)
    await asyncio.gather(db_da.connect(), cache_da.connect())

async def teardown(db_da: DatabaseDataAccess, cache_da: CacheDataAccess) -> None:
    await asyncio.gather(db_da.disconnect(), cache_da.disconnect())
