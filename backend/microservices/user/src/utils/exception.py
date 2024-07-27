from typing import Optional, Dict, Any
from ftgo_utils.errors import BaseError, ErrorCodes


async def handle_exception(
    e: Exception,
    error_code: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    message: Optional[str] = None,
    **kwargs,
) -> None:
    if isinstance(e, BaseError):
        raise e
    else:
        updated_payload = payload.copy() if payload else {}
        updated_payload.update(kwargs)
        base_exc = BaseError(
            error_code=error_code or ErrorCodes.UNKNOWN_ERROR,
            message=message or str(e),
            payload=updated_payload,
        )
        raise base_exc from e
