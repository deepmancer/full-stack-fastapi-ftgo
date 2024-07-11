
from typing import Optional
from fastapi import FastAPI

from config.auth import AuthConfig
from data_access.repository.cache_repository import CacheRepository
from utils.jwt_token import JWTTokenHandler
from middlewares.authentication.backend import JWTAuthenticationBackend
from schemas.authentication.user import UserSchema


def init_app(app: FastAPI, auth_config: Optional[AuthConfig] = None, cache_repository: Optional[CacheRepository] = None):
    cache_repository = CacheRepository() if cache_repository is None else cache_repository
    auth_config = AuthConfig() if auth_config is None else auth_config

    auth_backend = JWTAuthBackend(cache=cache_repository, config=auth_config)
    app.add_middleware(AuthenticationMiddleware, backend=auth_backend)
