from typing import Callable, Any, Dict
from functools import wraps
import traceback

from config import LayerNames, BaseConfig
from config.exceptions import BaseError
from ftgo_utils.logger import get_logger
from ftgo_utils.enums import ResponseStatus

def event_middleware(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Dict[str, Any]:
        logger = get_logger(layer_name=LayerNames.APP.value, environment=BaseConfig.load_environment())

        try:
            result = await func(*args, **kwargs)
            if not isinstance(result, dict):
                logger.warning(f"Expected result to be a dict, got {type(result)} instead.")
                result = {}
            
            result['status'] = ResponseStatus.SUCCESS.value
            return result

        except BaseError as e:
            logger.error(f"Domain error in {func.__name__}: {e.message}\n{traceback.format_exc()}")
            return {
                "status": ResponseStatus.FAILURE.value,
                "error_message": str(e.message),
            }
        
        except Exception as e:
            logger.error(f"Unhandled error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
            return {
                "status": ResponseStatus.ERROR.value,
                "error_message": str(e),
            }

    return wrapper
