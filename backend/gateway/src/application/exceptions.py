import time
from typing import Optional

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ftgo_utils.errors import ErrorCodes, BaseError, ErrorCategory, ErrorCategories
from application import get_logger


async def handle_exception(
    request: Request,
    exc: Exception,
    default_failure_message: Optional[str] = "An error occurred while processing the request",
) -> None:
    logger = get_logger()
    try:
        if isinstance(exc, BaseError):
            route_exc = exc
        else:
            route_exc = BaseError(
                error_code=ErrorCodes.INTERNAL_SERVER_ERROR,
                message=default_failure_message,
            )

        error_code = route_exc.error_code
        logger.error(
            f"Error processing request at {request.url} with request_id {request.state.request_id}",
            payload=route_exc.to_dict(),
        )

        common_fields = {
            "request_id": request.state.request_id,
            "path": request.url.path,
            "method": request.method,
            "timestamp": route_exc.timestamp,
        }

        if error_code.category == ErrorCategories.BUSINESS_LOGIC_ERROR:
            status_code = error_code.status_code or status.HTTP_400_BAD_REQUEST
            error_details = {
                "status_code": status_code,
                "error": error_code.value,
                "detail": error_code.description,
            }
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_details = {
                "status_code": status_code,
                "error": ErrorCodes.INTERNAL_SERVER_ERROR.value,
                "detail": route_exc.message or ErrorCodes.INTERNAL_SERVER_ERROR.description,
            }

        error_response = {**common_fields, **error_details}
        detail = jsonable_encoder(error_response)

        raise HTTPException(status_code=status_code, detail=detail)

    except HTTPException as http_exc:
        raise http_exc

    except Exception as unexpected_exc:
        logger.exception(
            f"Unexpected error processing request at {request.url} with request_id {request.state.request_id}",
            payload={"error": str(unexpected_exc), "detail": default_failure_message},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder({
                "request_id": request.state.request_id,
                "path": request.url.path,
                "method": request.method,
                "timestamp": int(time.time()),
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": ErrorCodes.INTERNAL_SERVER_ERROR.value,
                "detail": default_failure_message,
            }),
        )
