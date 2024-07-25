from typing import Callable, Any, Dict
from functools import wraps
import traceback

from config import LayerNames, BaseConfig
from application import get_logger, layer_name

from ftgo_utils.enums import ResponseStatus
from ftgo_utils.errors import ErrorCodes, BaseError

logger = get_logger()

def event_middleware(
    func: Callable,
) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            result = await func(*args, **kwargs)
            if not isinstance(result, dict):
                logger.warning(f"Expected result to be a dict, got {type(result)} instead.")
                result = {}

            result['status'] = ResponseStatus.SUCCESS.value
            return result

        except BaseError as e:
            logger.error(f"Error in {func.__name__} ({e.scope}): {e}")
            return {
                "status": ResponseStatus.FAILIURE.value,
                "error_code": e.error_code,
            }

        except Exception as e:
            logger.error(f"Unhandled error in {func.__name__} ({layer_name}):: {str(e)}")
            return {
                "status": ResponseStatus.ERROR.value,
                "error_code": ErrorCodes.UNKNOWN_ERROR,
            }

    return wrapper
