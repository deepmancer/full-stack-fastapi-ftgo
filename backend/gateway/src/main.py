import asyncio
import logging

import fastapi
import uvicorn

from config import ApplicationError

from ftgo_utils.logger import init_logging, get_logger

from application import app
from config import LayerNames
from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown
from data_access.broker import RPCBroker

service_config = ServiceConfig.load()

async def lifespan(app: fastapi.FastAPI):
    await setup()
    await RPCBroker.initialize(loop=asyncio.get_event_loop())

    init_logging(level=service_config.log_level)
    yield
    await teardown()

app = fastapi.FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=service_config.service_host,
        port=service_config.service_port,
        reload=True,
        log_level=service_config.log_level,
    )
