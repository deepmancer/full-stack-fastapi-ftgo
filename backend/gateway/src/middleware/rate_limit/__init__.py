from fastapi import FastAPI

from middleware.rate_limit.handler import (
    RateLimiter, _rate_limit_exceeded_handler, RateLimitExceeded,
)

def mount_middleware(app: FastAPI):
    app.state.limiter = RateLimiter()
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(
        RateLimiter.middleware_class(),
        **RateLimiter.middleware_kwargs(),
    )
