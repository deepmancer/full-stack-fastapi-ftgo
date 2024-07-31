from typing import Optional, List, Dict, Type, Union
from sqlalchemy.future import select

from asyncpg_client import AsyncPostgres
from ftgo_utils.errors import ErrorCodes
from config import PostgresConfig
from data_access import get_logger
from data_access.repository.base import BaseRepository
from data_access.models import Profile, Address, VehicleInfo, Base
from utils import handle_exception
from dto import BaseDTO, AddressDTO, ProfileDTO, VehicleDTO

class DatabaseRepository(BaseRepository):
    _data_access: Optional[AsyncPostgres] = None

    _dto_model_mapping: Dict[Type[BaseDTO], Type[Base]] = {
        ProfileDTO: Profile,
        AddressDTO: Address,
        VehicleDTO: VehicleInfo,
    }

    @classmethod
    async def initialize(cls) -> None:
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
            payload = db_config.dict()
            get_logger().error(ErrorCodes.DB_CONNECTION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DB_CONNECTION_ERROR, payload=payload)

    @classmethod
    async def fetch(
        cls,
        dto_class: Type[BaseDTO],
        query: Dict[str, Union[str, int, float]],
        one_or_none: bool = False,
        **kwargs
    ) -> Union[BaseDTO, List[BaseDTO], None]:
        model_class = cls._get_model_class(dto_class)
        try:
            async with cls._data_access.get_or_create_session() as session:
                result = await session.execute(select(model_class).filter_by(**query))
                if one_or_none:
                    instance = result.scalars().one_or_none()
                    return instance.to_dto() if instance else None
                return [instance.to_dto() for instance in result.scalars().all()]
        except Exception as e:
            payload = dict(model=model_class.__name__, query=query)
            get_logger().error(ErrorCodes.DB_FETCH_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DB_FETCH_ERROR, payload=payload)

    @classmethod
    async def insert(cls, dto_instances: Union[List[BaseDTO], BaseDTO], **kwargs) -> Union[BaseDTO, List[BaseDTO], None]:
        if not dto_instances:
            return None
        dto_instances = [dto_instances] if not isinstance(dto_instances, list) else dto_instances
        model_class = cls._get_model_class(type(dto_instances[0]))
        model_instances = [model_class.from_dto(dto) for dto in dto_instances]
        try:
            async with cls._data_access.get_or_create_session() as session:
                session.add_all(model_instances)
                await session.flush()
                await session.commit()
                for instance in model_instances:
                    await session.refresh(instance)
                casted_instances = [instance.to_dto() for instance in model_instances]
                return casted_instances[0] if len(casted_instances) == 1 else casted_instances
        except Exception as e:
            payload = dict(dto=[dto.to_dict() for dto in dto_instances])
            get_logger().error(ErrorCodes.DB_INSERT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DB_INSERT_ERROR, payload=payload)

    @classmethod
    async def update(
        cls,
        dto_class: Type[BaseDTO],
        query: Dict[str, Union[str, int, float]],
        update_fields: Dict[str, Union[str, int, float]],
        **kwargs
    ) -> Union[List[BaseDTO], None]:
        model_class = cls._get_model_class(dto_class)
        try:
            async with cls._data_access.get_or_create_session() as session:
                result = await session.execute(select(model_class).filter_by(**query))
                records = result.scalars().all()
                if not records:
                    return []
                for record in records:
                    for key, value in update_fields.items():
                        setattr(record, key, value)
                    if not session.is_modified(record):
                        session.add(record)
                await session.flush()
                await session.commit()
                for record in records:
                    await session.refresh(record)
                return [record.to_dto() for record in records]
        except Exception as e:
            payload = dict(model=model_class.__name__, query=query, update_fields=update_fields)
            get_logger().error(ErrorCodes.DB_UPDATE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DB_UPDATE_ERROR, payload=payload)

    @classmethod
    async def delete(cls, dto_class: Type[BaseDTO], query: Dict[str, Union[str, int, float]], **kwargs) -> Union[List[BaseDTO], None]:
        model_class = cls._get_model_class(dto_class)
        try:
            async with cls._data_access.get_or_create_session() as session:
                result = await session.execute(select(model_class).filter_by(**query))
                records = result.scalars().all()
                if not records:
                    return []
                dtos = [record.to_dto() for record in records]
                for record in records:
                    await session.delete(record)
                await session.commit()
                return dtos
        except Exception as e:
            payload = dict(model=model_class.__name__, query=query)
            get_logger().error(ErrorCodes.DB_DELETE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DB_DELETE_ERROR, payload=payload)

    @classmethod
    def _get_model_class(cls, dto: Union[BaseDTO, Type[BaseDTO]]) -> Type[Base]:
        if isinstance(dto, type):
            return cls._dto_model_mapping[dto]
        return cls._dto_model_mapping[type(dto)]
