import asyncio
import os
import uvloop
from dotenv import load_dotenv
from app import events
from utils.dynamic_port import get_dynamic_port

async def serve():
    # Load environment variables from .env file
    load_dotenv()
    
    container_name = os.getenv('USER_SERVICE_CONTAINER_NAME')
    internal_port = int(os.getenv('INTERNAL_PORT', 50051))
    
    grpc_port = get_dynamic_port(container_name, internal_port)
    print(f"gRPC server is starting on port {grpc_port}...")

    grpc_server = await events.create_grpc_server()
    grpc_server.add_insecure_port(f'[::]:{grpc_port}')
    await grpc_server.start()
    await grpc_server.wait_for_termination()

if __name__ == '__main__':
    uvloop.install()
    asyncio.run(serve())
