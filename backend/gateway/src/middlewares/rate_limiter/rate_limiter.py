# middlewares/rate_limit/rate_limit.py

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIASGIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from middlewares.base import BaseMiddleware

class RateLimiter:
    limiter = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RateLimiter, cls).__new__(cls)
            cls.limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])
        return cls.limiter
