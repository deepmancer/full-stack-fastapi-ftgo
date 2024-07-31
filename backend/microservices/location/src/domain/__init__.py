from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames

layer = LayerNames.DOMAIN.value

def get_logger(layer: str =layer):
    return _get_logger(layer=layer, env=ServiceConfig.load_environment())
