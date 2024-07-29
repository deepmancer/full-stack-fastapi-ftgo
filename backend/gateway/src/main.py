import asyncio
import contextlib

from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

from application.app import init_router
from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown
from ftgo_utils.logger import init_logging
from middleware.builder import MiddlewareBuilder

load_dotenv()

service_config = ServiceConfig()
init_logging(level=service_config.log_level)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await setup()

    yield

    await teardown()
    await RPCBroker.close()

app = FastAPI(
    title="Food Delivery Server",
    debug=service_config.debug,
    lifespan=lifespan,
)

app.include_router(init_router(), prefix=service_config.api_prefix)
middleware_builder = MiddlewareBuilder().add_rate_limit().add_cors().add_authentication()
middleware_builder.build(app=app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=service_config.service_host,
        port=service_config.service_port,
        reload=True,
        log_level=service_config.log_level,
    )
