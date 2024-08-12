from slowapi import Limiter
from slowapi.middleware import SlowAPIASGIMiddleware
from slowapi.util import get_remote_address


class RateLimiter:
    limiter = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RateLimiter, cls).__new__(cls)
            cls.limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])
        return cls.limiter

    @staticmethod
    def middleware_class():
        return SlowAPIASGIMiddleware

    @staticmethod
    def middleware_kwargs():
        return {}
