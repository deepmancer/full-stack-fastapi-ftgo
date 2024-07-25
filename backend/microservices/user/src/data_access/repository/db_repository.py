from typing import Optional, List, Dict, Type
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from asyncpg_client import AsyncPostgres
from ftgo_utils.errors import ErrorCodes

from config import PostgresConfig, DataAccessError
from data_access import get_logger, layer_name
from data_access.repository.base import BaseRepository
from models.base import Base
from utils.error_handler import handle_error

class DatabaseRepository(BaseRepository):
    _data_access: Optional[AsyncPostgres] = None

    @classmethod
    async def initialize(cls):
        db_config = PostgresConfig()
        try:
            pg_data_access = await AsyncPostgres.create(
                host=db_config.host,
                port=db_config.port,
                database=db_config.db,
                user=db_config.user,
                password=db_config.password,
                echo=db_config.enable_echo_log,
                expire_on_commit=db_config.enable_expire_on_commit,
            )
            async with pg_data_access._async_engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
                cls._data_access = pg_data_access

        except Exception as e:
            get_logger().error(f"Error connecting to database: config={db_config}, error={e}")
            return handle_error(e=e, error_code=ErrorCodes.DB_CONNECTION_ERROR, layer=layer_name)

    @classmethod
    async def fetch_by_query(cls, model: Type[Base], query: Dict[str, str], one_or_none: bool = False):
        try:
            async with cls._data_access.get_or_create_session() as session:
                result = await session.execute(select(model).filter_by(**query))
                if one_or_none:
                    return result.scalars().one_or_none()
                return result.scalars().all()
        except Exception as e:
            get_logger().error(f"Error fetching data from database: model={model.__name__}, query={query}, error={e}")
            return handle_error(e=e, error_code=ErrorCodes.DB_FETCH_ERROR, layer=layer_name)

    @classmethod
    async def insert(cls, model_instance: Base):
        try:
            async with cls._data_access.get_or_create_session() as session:
                session.add(model_instance)
                await session.flush()
                await session.commit()
                await session.refresh(model_instance)
                return model_instance
        except Exception as e:
            get_logger().error(f"Error inserting data into database: model_instance={model_instance.__dict__}, error={e}")
            await session.rollback()
            return handle_error(e=e, error_code=ErrorCodes.DB_INSERT_ERROR, layer=layer_name)

    @classmethod
    async def update_by_query(cls, model: Type[Base], query: Dict[str, str], update_fields: Dict[str, str]):
        try:
            async with cls._data_access.get_or_create_session() as session:
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
            get_logger().error(f"Error updating data in database: model={model.__name__}, query={query}, update_fields={update_fields}, error={e}")
            await session.rollback()
            return handle_error(e=e, error_code=ErrorCodes.DB_UPDATE_ERROR, layer=layer_name)

    @classmethod
    async def delete_by_query(cls, model: Type[Base], query: Dict[str, str]):
        try:
            async with cls._data_access.get_or_create_session() as session:
                result = await session.execute(select(model).filter_by(**query))
                records = result.scalars().all()

                if not records:
                    return None

                for record in records:
                    await session.delete(record)

                await session.commit()
                return records

        except Exception as e:
            get_logger().error(f"Error deleting data from database: model={model.__name__}, query={query}, error={e}")
            await session.rollback()
            return handle_error(e=e, error_code=ErrorCodes.DB_DELETE_ERROR, layer=layer_name)

    @classmethod
    async def terminate(cls):
        if cls._data_access:
            await cls._data_access.disconnect()
            cls._data_access = None
