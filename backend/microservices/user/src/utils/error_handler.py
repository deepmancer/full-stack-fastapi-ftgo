from ftgo_utils.errors import BaseError, ErrorCodes

from config.exceptions import get_error_class

def handle_error(e: Exception, error_code: str = None, layer: str = None):
    if isinstance(e, BaseError):
        raise e
    else:
        error_class = get_error_class(layer)
        error_code = error_code or ErrorCodes.UNKNOWN_ERROR
        raise error_class(error_code=error_code) from e
