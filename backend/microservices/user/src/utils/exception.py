from ftgo_utils.errors import BaseError, ErrorCodes
from typing import Optional, Dict, Any


def handle_exception(
    e: Exception,
    error_code: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    message: Optional[str] = None,
    **kwargs,
):
    if isinstance(e, BaseError):
        raise e
    else:
        updated_payload = payload or {}
        updated_payload.update(kwargs)
        raise BaseError(
            error_code=error_code or ErrorCodes.UNKNOWN_ERROR,
            message=message,
            payload=updated_payload,
        ) from e
