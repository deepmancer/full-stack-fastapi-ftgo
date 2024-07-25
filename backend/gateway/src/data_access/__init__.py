from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames

def get_logger(layer_name: str = LayerNames.DATA_ACCESS.value):
    return _get_logger(layer_name=layer_name, environment=ServiceConfig.load_environment())
