import traceback
import json

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder

from application import get_logger

from ftgo_utils.errors import ErrorCodes, BaseError

def register_error_handlers(app: FastAPI):
    logger = get_logger()

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        error_details = {
            "error": "HTTPException",
            "status_code": exc.status_code,
            "detail": exc.detail,
            "request_url": str(request.url)
        }
        logger.error(f"HTTP error occurred: {json.dumps(error_details)}", exc_info=True)
        return JSONResponse(status_code=exc.status_code, content=error_details)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        error_details = {
            "error": "RequestValidationError",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": exc.errors(),
            "body": exc.body,
            "request_url": str(request.url)
        }
        logger.error(f"Validation error occurred: {json.dumps(error_details)}", exc_info=True)
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(error_details))

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        error_details = {
            "error": "Exception",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "Internal server error",
            "request_url": str(request.url)
        }
        logger.error(f"Unexpected error occurred: {traceback.format_exc()}", exc_info=True)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_details)

    @app.exception_handler(UserAuthenticationError)
    async def authentication_error_handler(request: Request, exc: UserAuthenticationError):
        error_details = {
            "error": exc.__class__.__name__,
            "status_code": exc.status_code,
            "detail": exc.detail,
            "request_url": str(request.url)
        }
        logger.error(f"JWT authentication error occurred: {json.dumps(error_details)}", exc_info=True)
        return JSONResponse(status_code=exc.status_code, content=error_details)
