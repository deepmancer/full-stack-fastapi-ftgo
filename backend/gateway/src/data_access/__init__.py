import loguru
from config.enums import LayerNames
from utils.logger import LoggerFactory

def get_logger() -> loguru.logger:
    return LoggerFactory.get_logger(layer_name=LayerNames.DATA_ACCESS.value)
