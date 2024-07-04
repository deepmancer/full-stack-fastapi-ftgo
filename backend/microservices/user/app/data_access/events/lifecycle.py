# app/data_access/services/lifecycle.py

import asyncio
from data_access.session.db import DatabaseSession
from data_access.session.cache import CacheSession

async def setup(db_config, cache_config):
    db_da = DatabaseSession(db_config)
    cache_da = CacheSession(cache_config)
    await asyncio.gather(db_da.connect(), cache_da.connect())
    return db_da, cache_da

async def teardown(db_da, cache_da):
    await asyncio.gather(db_da.disconnect(), cache_da.disconnect())
