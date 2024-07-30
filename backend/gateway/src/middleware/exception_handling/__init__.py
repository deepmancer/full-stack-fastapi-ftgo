from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from middleware.exception_handling.handler import validation_exception_handler


def mount_middleware(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
