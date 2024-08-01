from fastapi import FastAPI

from middleware.request_id.handler import RequestUUIDMiddleware

def mount_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestUUIDMiddleware)
