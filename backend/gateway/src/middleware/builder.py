# gateway/src/middleware/builder.py

from typing import List, Callable

from fastapi import FastAPI
from middleware.authentication import mount_middleware as mount_authentication
from middleware.cors import mount_middleware as mount_cors
from middleware.exception_handling import mount_middleware as mount_exception_handling
from middleware.https_redirect import mount_middleware as mount_https_redirect
from middleware.logger import mount_middleware as mount_logger
from middleware.rate_limit import mount_middleware as mount_rate_limit
from middleware.request_id import mount_middleware as mount_request_id
from middleware.timing import mount_middleware as mount_timing


class MiddlewareBuilder:
    def __init__(self) -> None:
        self._middlewares: List[Callable[[FastAPI], None]] = []

    def add_cors(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_cors)
        return self

    def add_rate_limit(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_rate_limit)
        return self

    def add_authentication(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_authentication)
        return self

    def add_exception_handling(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_exception_handling)
        return self

    def add_https_redirect(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_https_redirect)
        return self

    def add_timing(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_timing)
        return self

    def add_logger(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_logger)
        return self

    def add_request_id(self) -> 'MiddlewareBuilder':
        self._middlewares.append(mount_request_id)
        return self

    def build(self, app: FastAPI) -> None:
        for middleware in self._middlewares:
            middleware(app)
