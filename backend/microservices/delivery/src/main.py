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
from application.routes import address_router, profile_router, vehicle_router

from ftgo_utils.logger import init_logging, get_logger

from config import LayerNames
from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown

# Load the configuration
service_config = ServiceConfig.load()

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=profile_router, prefix=service_config.api_prefix)
app.include_router(router=address_router, prefix=service_config.api_prefix)
app.include_router(router=vehicle_router, prefix=service_config.api_prefix)

@app.on_event("startup")
async def startup_event():
    await setup()
    init_logging(level=service_config.log_level)

@app.on_event("shutdown")
async def shutdown_event():
    await teardown()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    get_logger(LayerNames.APP.value).error(f"{exc}")
    return await request_validation_exception_handler(request, exc)

if __name__ == "__main__":
    init_logging(level=service_config.log_level)
  
    uvicorn.run(
        "main:app",
        host=service_config.service_host,
        port=service_config.service_port,
        reload=True,
        log_level=service_config.log_level,
    )
