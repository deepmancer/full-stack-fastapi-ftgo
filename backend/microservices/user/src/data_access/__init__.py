from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames

def get_logger():
    return _get_logger(LayerNames.DATA_ACCESS.value, ServiceConfig.environment)
