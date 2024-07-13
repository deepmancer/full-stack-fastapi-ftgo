import contextlib
from typing import Optional, Dict, Type
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.future import select

from config.db import PostgresConfig
from models.base import Base
from data_access.resources.base import BaseDataAccess
from data_access import get_logger
from data_access.exceptions import (
    DatabaseConnectionError,
    DatabaseSessionCreationError,
    DatabaseInsertError,
    DatabaseFetchError,
    DatabaseUpdateError,
    DatabaseDeleteError
)

class DatabaseDataAccess(BaseDataAccess):
    _config: Optional[PostgresConfig] = None

    def __init__(self, config: PostgresConfig):
        self._config = config

        self._async_engine: AsyncEngine = self._create_async_engine()
        self._async_session_maker = self._create_async_session_maker()

    
    def _create_async_engine(self) -> AsyncEngine:
        return create_async_engine(
            url=self._config.async_url,
            echo=self._config.enable_echo_log,
        )

    def _create_async_session_maker(self) -> async_sessionmaker:
        return async_sessionmaker(
            bind=self._async_engine,
            expire_on_commit=self._config.enable_expire_on_commit,
            class_=AsyncSession,
        )

    @contextlib.asynccontextmanager
    async def get_or_create_session(self):
        session = self._async_session_maker()
        try:
            yield session
        except Exception as e:
            self.logger.error(f"Failed to create session for Postgres at {self._config.async_url}: {e}")
            await session.rollback()
            raise DatabaseSessionCreationError() from e
        finally:
            await session.close()

    async def connect(self) -> None:
        try:
            async with self._async_engine.begin() as connection:
                await connection.run_sync(lambda conn: None)
        except Exception as e:
            self.logger.error(f"Failed to connect to Postgres at {self._config.async_url}: {e}")
            raise DatabaseConnectionError(self._config.async_url) from e

    async def disconnect(self) -> None:
        await self._async_engine.dispose()
