import asyncio
import uvloop
from grpc.aio import server
from grpc_interface import user_service_pb2_grpc
from grpc_interface.user_service import UserServiceServicer
from application.user_handler import UserHandler
from domain.user import UserService
from data_access.repository.user import UserRepository
from data_access.postgres.session import PostgresSession
from data_access.redis.session import RedisSession
from configs.postgres import PostgresConfig
from configs.redis import RedisConfig
from app.interceptors import get_interceptors

async def create_grpc_server():
    postgres_config = PostgresConfig()
    redis_config = RedisConfig()

    postgres_session = PostgresSession(postgres_config)
    await postgres_session.initialize()

    redis_session = RedisSession(redis_config)
    await redis_session.initialize()

    user_repository = UserRepository(postgres_session.get_session())
    user_service = UserService(user_repository, redis_session)
    user_handler = UserHandler(user_service)
    user_service_servicer = UserServiceServicer(user_handler)

    interceptors = get_interceptors()

    grpc_server = server(asyncio.get_event_loop(), interceptors=interceptors)
    user_service_pb2_grpc.add_UserServiceServicer_to_server(user_service_servicer, grpc_server)
    return grpc_server

async def serve():
    grpc_server = await create_grpc_server()
    await grpc_server.start()
    await grpc_server.wait_for_termination()
