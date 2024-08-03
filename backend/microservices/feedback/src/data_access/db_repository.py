from typing import Optional
from beanie import init_beanie
from mongo_motors import AsyncMongo

from ftgo_utils.errors import ErrorCodes

from config import MongoConfig
from data_access import get_logger
from data_access.base import BaseRepository
from models import OrderRating, DeliveryRating
from utils import handle_exception

class DatabaseRepository(BaseRepository):
    _data_access: Optional[AsyncMongo] = None

    @classmethod
    async def initialize(cls) -> None:
        db_config = MongoConfig()
        try:
            mongo_data_access = await AsyncMongo.create(
                host=db_config.host,
                port=db_config.port,
                database=db_config.database,
                username=db_config.username,
                password=db_config.password,
            )
            await init_beanie(
                database=mongo_data_access.get_database(),
                document_models=[OrderRating, DeliveryRating],
            )
            cls._data_access = mongo_data_access

        except Exception as e:
            payload = db_config.dict()
            get_logger().error(ErrorCodes.DB_CONNECTION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DB_CONNECTION_ERROR, payload=payload)

    @classmethod
    async def terminate(cls) -> None:
        if cls._data_access:
            await cls._data_access.disconnect()
            cls._data_access = None
