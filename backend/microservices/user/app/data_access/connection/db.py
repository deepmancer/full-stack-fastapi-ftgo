import contextlib
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy import MetaData, Table

from typing import Optional, Dict, Type
from loguru import logger

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from config.db import PostgresConfig
from data_access.models.base import Base
from data_access.connection.base import BaseDataAccess

class DatabaseDataAccess(BaseDataAccess):
    _config: Optional[PostgresConfig] = None

    def __init__(self, config: PostgresConfig):
        self.initialize(config)
        self.async_engine: AsyncEngine = create_async_engine(
            url=self._config.async_url,
            echo=self._config.enable_echo_log,
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=self._config.enable_expire_on_commit,
            class_=AsyncSession,
        )

    @contextlib.asynccontextmanager
    async def get_or_create_session(self):
        session = self.async_session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def connect(self) -> None:
        async with self.async_engine.begin() as connection:
            await connection.run_sync(lambda conn: None)

    async def disconnect(self) -> None:
        await self.async_engine.dispose()

    async def load_from_table_by_query(self, model: Type[Base], query: Dict[str, str], one_or_none: bool = False):
        async with self.get_or_create_session() as session:
            try:
                result = await session.execute(
                    select(model).filter_by(**query)
                )
                if one_or_none:
                    return result.scalars().one_or_none()
                return result.scalars().all()
            except Exception as e:
                message = f"Error occurred while loading records: {e}"
                logger.error(message, model=model, query=query, one_or_none=one_or_none)
                raise e

    async def update_table_by_query(self, model: Type[Base], query: Dict[str, str], update_fields: Dict[str, str]):
        async with self.get_or_create_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        select(model).filter_by(**query)
                    )
                    records = result.scalars().all()
                    
                    if not records:
                        logger.info(f"No records found for query: {query}")
                        return None

                    for record in records:
                        for key, value in update_fields.items():
                            setattr(record, key, value)
                        
                    await session.commit()
                    return records

            except Exception as e:
                await session.rollback()
                message = f"Error occurred while updating records: {e}"
                logger.error(message, model=model, query=query, update_fields=update_fields)
                raise e

    async def delete_from_table_by_query(self, model: Type[Base], query: Dict[str, str]):
        async with self.get_or_create_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        select(model).filter_by(**query)
                    )
                    records = result.scalars().all()
                    
                    if not records:
                        logger.info(f"No records found for query: {query}")
                        return None

                    for record in records:
                        await session.delete(record)
                        
                    await session.commit()
                    return records

            except Exception as e:
                await session.rollback()
                message = f"Error occurred while deleting records: {e}"
                logger.error(message, model=model, query=query)
                raise e
