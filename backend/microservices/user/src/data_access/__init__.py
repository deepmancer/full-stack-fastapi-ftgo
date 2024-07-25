from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames
from utils.error_handler import handle_error as _handle_error

layer_name = LayerNames.DATA_ACCESS.value

def get_logger(layer_name: str = layer_name):
    return _get_logger(layer_name=layer_name, environment=ServiceConfig.load_environment())
