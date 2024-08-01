from fastapi import FastAPI

from middleware.logger.handler import LoggingMiddleware

def mount_middleware(app: FastAPI) -> None:
    app.add_middleware(LoggingMiddleware)
