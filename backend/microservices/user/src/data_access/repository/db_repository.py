from typing import Optional, List, Dict, Type
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from asyncpg_client import AsyncPostgres

from config.db import PostgresConfig
from models.base import Base
from data_access.repository.base import BaseRepository
from data_access.exceptions import *

class DatabaseRepository(BaseRepository):
    data_access: Optional[AsyncPostgres] = None

    @classmethod
    async def initialize(cls):
        db_config = PostgresConfig()
        cls.data_access = await AsyncPostgres.create(
            host=db_config.host,
            port=db_config.port,
            database=db_config.db,
            user=db_config.user,
            password=db_config.password,
            echo=db_config.enable_echo_log,
            expire_on_commit=db_config.enable_expire_on_commit,
        )

    @classmethod
    async def fetch_by_query(cls, model: Type[Base], query: Dict[str, str], one_or_none: bool = False):
        async with cls.data_access.get_or_create_session() as session:
            try:
                result = await session.execute(select(model).filter_by(**query))
                if one_or_none:
                    return result.scalars().one_or_none()
                return result.scalars().all()
            except Exception as e:
                raise DatabaseFetchError(query) from e

    @classmethod
    async def insert(cls, model_instance: Base):
        async with cls.data_access.get_or_create_session() as session:
            try:
                session.add(model_instance)
                await session.flush()
                await session.commit()
                await session.refresh(model_instance)
                return model_instance
            except Exception as e:
                await session.rollback()
                raise DatabaseInsertError(model_instance.__dict__) from e

    @classmethod
    async def update_by_query(cls, model: Type[Base], query: Dict[str, str], update_fields: Dict[str, str]):
        async with cls.data_access.get_or_create_session() as session:
            try:
                result = await session.execute(select(model).filter_by(**query))
                records = result.scalars().all()

                if not records:
                    return None

                for record in records:
                    for key, value in update_fields.items():
                        setattr(record, key, value)
                    if not session.is_modified(record):
                        session.add(record)
                    await session.flush()

                await session.commit()
                
                for record in records:
                    await session.refresh(record)
                
                return records
            except Exception as e:
                await session.rollback()
                raise DatabaseUpdateError(query, update_fields) from e

    @classmethod
    async def delete_by_query(cls, model: Type[Base], query: Dict[str, str]):
        async with cls.data_access.get_or_create_session() as session:
            try:
                result = await session.execute(select(model).filter_by(**query))
                records = result.scalars().all()

                if not records:
                    return None

                for record in records:
                    await session.delete(record)

                await session.commit()
                return records

            except Exception as e:
                await session.rollback()
                raise DatabaseDeleteError(query) from e

    @classmethod
    async def terminate(cls):
        await cls.data_access.disconnect()