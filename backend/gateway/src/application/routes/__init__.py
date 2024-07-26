from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames

def get_logger(layer: str = LayerNames.GATEWAY.value):
    return _get_logger(layer=layer, env=ServiceConfig.load_environment())
