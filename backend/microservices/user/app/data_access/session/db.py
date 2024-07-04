from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.pool import QueuePool
from configs.db import PostgresConfig
from data_access.session.base import BaseDataAccess
from typing import AsyncGenerator, Optional

class DatabaseDataAccess(BaseDataAccess):
    _config: Optional[PostgresConfig] = None

    def __init__(self, config: PostgresConfig):
        super().initialize(config)
        self.async_engine: AsyncEngine = create_async_engine(
            url=self._config.async_url,
            echo=self._config.enable_echo_log,
            pool_size=self._config.pool_size,
            max_overflow=self._config.pool_overflow,
            poolclass=QueuePool,
            connect_args={"connect_timeout": self._config.timeout},
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=self._config.enable_expire_on_commit,
            class_=AsyncSession,
        )

    async def get_or_create_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session

    async def connect(self) -> None:
        async with self.async_engine.begin() as connection:
            await connection.run_sync(lambda conn: None)

    async def disconnect(self) -> None:
        await self.async_engine.dispose()