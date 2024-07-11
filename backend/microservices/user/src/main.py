import os
import fastapi
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from config.exceptions import ApplicationError
from application.routes.profile import router as user_profile_router
from application.routes.address import router as address_router

from config.logger import init_logging
from utils.logger import LoggerFactory
from config.enums import LayerNames
from data_access.events.lifecycle import setup, teardown

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_profile_router, prefix=os.getenv("API_PREFIX", ""))
app.include_router(router=address_router, prefix=os.getenv("API_PREFIX", ""))

@app.on_event("startup")
async def startup_event():
    await setup()
    init_logging()

@app.on_event("shutdown")
async def shutdown_event():
    await teardown()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    LoggerFactory.get_logger(LayerNames.APP.value).error(f"{exc}")
    return await request_validation_exception_handler(request, exc)


if __name__ == "__main__":
    init_logging()
  
    host = os.getenv("SERVICE_HOST", "127.0.0.1")
    port = int(os.getenv("SERVICE_PORT", 5020))
    debug = os.getenv("DEBUG", "True").lower() in ["true", "1", "t"]

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="debug" if debug else "info",
    )
