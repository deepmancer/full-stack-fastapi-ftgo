from fastapi import Request
from middleware import get_logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        get_logger().info(f"API {request.url} with request_id {request.state.request_id} was called")
        return await call_next(request)
