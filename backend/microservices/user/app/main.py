import os
import fastapi
import uvicorn
from loguru import logger

from fastapi.middleware.cors import CORSMiddleware

from config.logger import init_logging
from application.endpoints import app as api_endpoint_router
from data_access.events.lifecycle import setup, teardown

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_endpoint_router, prefix=os.getenv("API_PREFIX", "/user"))

@app.on_event("startup")
async def startup_event():
    await setup()
    init_logging()

@app.on_event("shutdown")
async def shutdown_event():
    await teardown()


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
