from fastapi import Request
from ftgo_utils.uuid_gen import uuid4
from starlette.middleware.base import BaseHTTPMiddleware


class RequestUUIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
