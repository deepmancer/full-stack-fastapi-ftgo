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

from config import LayerNames, ServiceConfig

from application.routes.auth import router as auth_router

import middlewares.rate_limiter as rate_limiter
import middlewares.authentication as auth_middleware
import middlewares.cors as cors_middleware

service_config = ServiceConfig.load()

app = fastapi.FastAPI(
    debug=service_config.debug,
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    get_logger(LayerNames.GATEWAY.value).error(f"{exc}")
    return await request_validation_exception_handler(request, exc)

cors_middleware.mount_middleware(app)
rate_limiter.mount_middleware(app)

app.include_router(router=auth_router, prefix=service_config.api_prefix)
