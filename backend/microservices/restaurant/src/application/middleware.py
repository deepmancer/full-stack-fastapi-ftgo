from typing import Callable, Any, Dict
from functools import wraps

from config import LayerNames, BaseConfig
from application import get_logger

from ftgo_utils.enums import ResponseStatus
from ftgo_utils.errors import ErrorCodes, BaseError, ErrorCategories

logger = get_logger()

def event_middleware(event_name: str, func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            result = await func(*args, **kwargs)
            if not isinstance(result, dict) or not result:
                logger.warning(f"Expected result to be a dict, got {type(result)} instead.")
                result = {}

            result['status'] = ResponseStatus.SUCCESS.value
            return result

        except BaseError as e:
            logger.exception(f"Error in {event_name}: {e.error_code.value}", payload=e.to_dict())
            error_code = e.error_code
            if error_code.category != ErrorCategories.BUSINESS_LOGIC_ERROR:
                error_code = ErrorCodes.UNKNOWN_ERROR
            return {
                "status": ResponseStatus.FAILURE.value,
                "error_code": error_code.value,
            }

        except Exception as e:
            logger.exception(f"Error in {event_name}: {ErrorCodes.UNKNOWN_ERROR.value}", payload={"error": str(e)})
            return {
                "status": ResponseStatus.ERROR.value,
                "error_code": ErrorCodes.UNKNOWN_ERROR.value,
            }

    return wrapper
