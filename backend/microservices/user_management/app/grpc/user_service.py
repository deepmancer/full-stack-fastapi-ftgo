import grpc
from concurrent import futures
from app.grpc_interface import user_pb2, user_pb2_grpc
from app.application.user_handler import UserHandler
from uuid import UUID
from prometheus_client import Summary
import logging

logger = logging.getLogger(__name__)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class UserServiceGRPC(user_pb2_grpc.UserServicer):
    def __init__(self):
        self.user_handler = UserHandler()

    @REQUEST_TIME.time()
    async def CreateUser(self, request, context):
        logger.info(f"Received CreateUser request for email: {request.email}")
        user = await self.user_handler.create_user(
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            email=request.email,
            password=request.password
        )
        logger.info(f"User created with email: {user.email}")
        return user_pb2.UserResponse(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            email=user.email,
            email_verified=user.email_verified,
            phone_number_verified=user.phone_number_verified,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )

    @REQUEST_TIME.time()
    async def GetUser(self, request, context):
        logger.info(f"Received GetUser request for id: {request.id}")
        user = await self.user_handler.get_user_by_id(UUID(request.id))
        if not user:
            logger.error(f"User not found for id: {request.id}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_pb2.UserResponse()
        logger.info(f"User retrieved with email: {user.email}")
        return user_pb2.UserResponse(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            email=user.email,
            email_verified=user.email_verified,
            phone_number_verified=user.phone_number_verified,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )

def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServiceGRPC(), server)
    server.add_insecure_port('[::]:50051')
    logger.info("Starting gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
