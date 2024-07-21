from typing import Optional
from fastapi import FastAPI

from config import AuthConfig
from data_access.repository import CacheRepository
from middlewares.authentication.backend import JWTAuthenticationBackend


def mount_middleware(
    app: FastAPI,
    auth_config: Optional[AuthConfig] = None,
    cache_repository: Optional[CacheRepository] = None,
):
    app.add_middleware(
        JWTAuthenticationBackend.middleware_class(),
        **JWTAuthenticationBackend.middleware_kwargs(auth_config=auth_config, cache_repository=cache_repository),
    )
