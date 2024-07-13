import loguru
from config.enums import LayerNames
from config.logger_factory import LoggerFactory

def get_logger() -> loguru.logger:
    return LoggerFactory.get_logger(layer_name=LayerNames.DATA_ACCESS.value)
