from config import LayerNames
from ftgo_utils.logger import get_logger as _get_logger

def get_logger():
    return _get_logger(LayerNames.APP.value)
