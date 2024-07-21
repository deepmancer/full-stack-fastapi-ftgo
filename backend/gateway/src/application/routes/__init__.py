from config import LayerNames, ServiceConfig

from ftgo_utils.logger import get_logger as _get_logger

def get_logger():
    return _get_logger(layer_name=LayerNames.GATEWAY.value, environment=ServiceConfig.load_environment())

