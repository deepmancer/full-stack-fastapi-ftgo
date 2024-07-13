import loguru

from ftgo_utils.logger import get_logger as _get_logger

from config import LayerNames

def get_logger() -> loguru.logger:
    return _get_logger(LayerNames.DATA_ACCESS.value)
