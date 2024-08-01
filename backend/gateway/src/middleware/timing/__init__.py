from fastapi import FastAPI

from middleware.timing.handler import ProcessTimeMiddleware

def mount_middleware(app: FastAPI) -> None:
    app.add_middleware(ProcessTimeMiddleware)
