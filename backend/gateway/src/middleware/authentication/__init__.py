from fastapi import FastAPI
from middleware.authentication.auth_middleware import JWTAuthenticationMiddleware

def mount_middleware(app: FastAPI):
    app.add_middleware(JWTAuthenticationMiddleware)
