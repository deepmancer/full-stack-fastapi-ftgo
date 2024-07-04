from sqlalchemy.ext.asyncio import (
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    create_async_engine as create_sqlalchemy_async_engine,
)
from sqlalchemy.pool import QueuePool as SQLAlchemyQueuePool

from data_access.session.interface import AsyncSessionInterface
from configs.db import PostgresConfig

class DatabaseSession(AsyncSessionInterface):
    def __init__(self, config: PostgresConfig):
        self.config = config
        self.async_engine = create_sqlalchemy_async_engine(
            url=self.config.async_url,
            echo=self.config.enable_echo_log,
            pool_size=self.config.pool_size,
            max_overflow=self.config.pool_overflow,
            poolclass=SQLAlchemyQueuePool,
            connect_args={"connect_timeout": self.config.timeout},
        )
        self.async_session_maker = sqlalchemy_async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=self.config.enable_expire_on_commit,
            class_=SQLAlchemyAsyncSession,
        )
        self.async_session = None

    async def get_or_create_session(self):
        async with self.async_session_maker() as session:
            yield session

    async def connect(self):
        async with self.async_engine.begin() as connection:
            await connection.run_sync(lambda conn: None)

    async def disconnect(self, backend_app):
        await self.async_engine.dispose()
