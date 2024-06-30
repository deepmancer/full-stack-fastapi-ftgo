import uvloop
import asyncio
from app.data_access.init_db import init_db
from app.grpc.user_service import serve
from app.configs.logging import setup_logging
from prometheus_client import start_http_server, Summary
import logging
from foodzood.backend.microservices.user_management.app.data_access.redis.redis_client import redis_client

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize uvloop
uvloop.install()

# Initialize Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Health check endpoint
async def health_check():
    logger.info("Health check endpoint called.")
    return {"status": "healthy"}

async def main():
    logger.info("Starting gRPC server...")
    start_http_server(8000)
    await init_db()
    logger.info("Database initialized.")
    await serve()

if __name__ == "__main__":
    logger.info("Starting the application...")
    asyncio.run(main())
