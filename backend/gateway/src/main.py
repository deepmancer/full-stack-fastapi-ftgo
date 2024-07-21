import logging

import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError

from config import ApplicationError

from ftgo_utils.logger import init_logging, get_logger

from config import LayerNames
from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown

from application import app

service_config = ServiceConfig.load()

@app.on_event("startup")
async def startup_event():
    await setup()
    init_logging(level=service_config.log_level)

@app.on_event("shutdown")
async def shutdown_event():
    await teardown()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=service_config.service_host,
        port=service_config.service_port,
        reload=True,
        log_level=service_config.log_level,
    )
