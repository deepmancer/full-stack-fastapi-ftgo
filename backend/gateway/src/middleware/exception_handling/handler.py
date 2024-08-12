import time

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    common_fields = {
        "path": request.url.path,
        "timestamp": int(time.time()),
        "method": request.method,
    }

    error_details = {
        **common_fields,
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "detail": exc.errors(),
        "body": exc.body
    }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(error_details),
    )
