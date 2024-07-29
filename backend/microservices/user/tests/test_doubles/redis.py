import asyncio
import time
from contextlib import asynccontextmanager
from typing import Optional, Dict, List, Tuple, Callable

class FakeAsyncRedisSession:
    def __init__(self, store: Dict[str, str], expiry_store: Dict[str, float], time_provider: Callable = time.time):
        self.store = store
        self.expiry_store = expiry_store
        self.time_provider = time_provider

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, key: str) -> Optional[str]:
        current_time = self.time_provider()
        if key in self.expiry_store and self.expiry_store[key] < current_time:
            await self.delete(key)
            return None
        return self.store.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None):
        self.store[key] = value
        if ex is not None:
            self.expiry_store[key] = self.time_provider() + ex

    async def delete(self, key: str):
        self.store.pop(key, None)
        self.expiry_store.pop(key, None)

    async def expire(self, key: str, ttl: int):
        if key in self.store:
            self.expiry_store[key] = self.time_provider() + ttl

    async def flushdb(self):
        self.store.clear()
        self.expiry_store.clear()

    def pipeline(self):
        return FakeRedisPipeline(self.store, self.expiry_store, self.time_provider)

class FakeAsyncRedis:
    def __init__(self):
        self.store = {}
        self.expiry_store = {}
        self.time_provider = time.time

    @asynccontextmanager
    async def get_or_create_session(self):
        session = FakeAsyncRedisSession(self.store, self.expiry_store, self.time_provider)
        yield session

    async def disconnect(self):
        pass

    @classmethod
    async def create(
        cls,
        host: str,
        port: int,
        db: int,
        password: Optional[str] = None,
        time_provider: Callable = time.time,
        **kwargs,
    ):
        instance = cls()
        instance.time_provider = time_provider
        return instance

class FakeRedisPipeline:
    def __init__(self, store: Dict[str, str], expiry_store: Dict[str, float], time_provider: Callable = time.time):
        self.store = store
        self.expiry_store = expiry_store
        self.time_provider = time_provider
        self.commands: List[Tuple[Callable, Tuple]] = []

    async def execute(self):
        results = []
        for method, args in self.commands:
            result = await method(*args)
            results.append(result)
        self.commands = []
        return results

    def delete(self, key: str):
        self.commands.append((self._delete_key, (key,)))
        return self

    async def _delete_key(self, key: str):
        self.store.pop(key, None)
        self.expiry_store.pop(key, None)

    def set(self, key: str, value: str, ex: Optional[int] = None):
        self.commands.append((self._set_key, (key, value, ex)))
        return self

    async def _set_key(self, key: str, value: str, ex: Optional[int] = None):
        self.store[key] = value
        if ex is not None:
            self.expiry_store[key] = self.time_provider() + ex

    def get(self, key: str):
        self.commands.append((self._get_key, (key,)))
        return self

    async def _get_key(self, key: str):
        current_time = self.time_provider()
        if key in self.expiry_store and self.expiry_store[key] < current_time:
            await self._delete_key(key)
            return None
        return self.store.get(key)

    def expire(self, key: str, ttl: int):
        self.commands.append((self._expire_key, (key, ttl)))
        return self

    async def _expire_key(self, key: str, ttl: int):
        if key in self.store:
            self.expiry_store[key] = self.time_provider() + ttl
