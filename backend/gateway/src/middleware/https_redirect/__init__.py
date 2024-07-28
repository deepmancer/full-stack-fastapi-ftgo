from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


def mount_middleware(app: FastAPI):
    app.add_middleware(HTTPSRedirectMiddleware)
