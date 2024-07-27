import asyncio
import contextlib
import logging

from dotenv import load_dotenv
import fastapi
import uvicorn

from application.app import init_router
from application.error_handlers import register_error_handlers
from config import LayerNames, ServiceConfig
from data_access.broker import RPCBroker
from data_access.events.lifecycle import setup, teardown
from ftgo_utils.logger import init_logging, get_logger
from middleware import rate_limiter, cors, authentication

load_dotenv()

service_config = ServiceConfig()
init_logging(level=service_config.log_level)

async def lifespan(app: fastapi.FastAPI):
    await setup()
    await RPCBroker.initialize(loop=asyncio.get_event_loop())

    yield

    await teardown()
    await RPCBroker.close()

app = fastapi.FastAPI(
    title="Food Delivery Server",
    debug=service_config.debug,
    lifespan=lifespan,
)

app.include_router(init_router(), prefix=service_config.api_prefix)
authentication.mount_middleware(app=app)
rate_limiter.mount_middleware(app=app)
cors.mount_middleware(app=app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=service_config.service_host,
        port=service_config.service_port,
        reload=True,
        log_level=service_config.log_level,
    )
