from config.enums import LayerNames
from utils.logger import LoggerFactory

def get_logger():
    return LoggerFactory.get_logger(layer_name=LayerNames.APP.value)
