from fastapi import FastAPI

from middlewares.rate_limiter.rate_limiter import (
    RateLimiter, _rate_limit_exceeded_handler, SlowAPIASGIMiddleware, RateLimitExceeded,
)

def init_app(cls, app: FastAPI):
    app.state.limiter = RateLimiter()
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIASGIMiddleware)
