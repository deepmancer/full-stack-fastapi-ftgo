from config import LayerNames, ServiceConfig

from ftgo_utils.logger import get_logger as _get_logger

def get_logger(layer_name=LayerNames.GATEWAY.value):
    return _get_logger(layer_name=layer_name, environment=ServiceConfig.load_environment())
