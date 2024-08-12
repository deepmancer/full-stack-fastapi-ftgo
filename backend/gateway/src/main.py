import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from ftgo_utils.logger import init_logging, get_logger
from prometheus_fastapi_instrumentator import Instrumentator

from application.app import init_router
from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown
from middleware.builder import MiddlewareBuilder

load_dotenv()

service_config = ServiceConfig()
init_logging(level=service_config.log_level)

async def lifespan(app: FastAPI):
    await setup()

    yield

    await teardown()

app = FastAPI(
    title="Food Delivery Server",
    debug=service_config.debug,
    lifespan=lifespan,
)

app.include_router(init_router(), prefix=service_config.api_prefix)
Instrumentator().instrument(app).expose(app)
middleware_builder = (
    MiddlewareBuilder()
    .add_rate_limit()
    .add_authentication()
    .add_logger()
    .add_request_id()
    .add_exception_handling()
    .add_timing()
    .add_cors()
)

middleware_builder.build(app=app)
if __name__ == "__main__":
    load_dotenv()

    service_config = ServiceConfig()
    init_logging(level=service_config.log_level)
    get_logger().info("Running the Gateway Service")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level=10, reload=True)