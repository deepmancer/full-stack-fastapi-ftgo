import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from configs.postgres import PostgresConfig

class PostgresSession:
    def __init__(self, config: PostgresConfig):
        self.config = config
        self.engine = None
        self.SessionLocal = None

    async def initialize(self):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.db}",
            echo=True
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession
        )

    async def get_session(self):
        async with self.SessionLocal() as session:
            yield session

    async def close(self):
        if self.engine:
            await self.engine.dispose()
