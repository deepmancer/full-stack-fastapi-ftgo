# app/events.py

import asyncio
from dotenv import load_dotenv

from application.handler import UserHandler
from domain.user import UserDomain
from data_access.crud.address import UserRepository
from data_access.session.db import PostgresSession
from data_access.session.cache import RedisSession
from configs.db import PostgresConfig
from configs.cache import RedisConfig

async def initialize_services():
    
    postgres_config = PostgresConfig()
    redis_config = RedisConfig()

    postgres_session = PostgresSession(postgres_config)
    await postgres_session.initialize()

    redis_session = RedisSession(redis_config)
    await redis_session.initialize()

    user_repository = UserRepository(postgres_session.get_session)
    user_service = User(user_repository, redis_session)
    user_handler = UserHandler(user_service)
    
    return user_handler

user_handler = asyncio.run(initialize_services())

events = {
    "register": user_handler.register,
    "authenticate_phone_number": user_handler.authenticate_phone_number,
    "login": user_handler.login,
    "get_user_info": user_handler.get_user_info,
    "add_address": user_handler.add_address,
    "modify_address": user_handler.modify_address,
    "delete_address": user_handler.delete_address,
    "set_preferred_address": user_handler.set_preferred_address,
}
