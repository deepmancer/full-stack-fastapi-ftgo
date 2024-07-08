from config.enums import LayerNames

class LoggerFactory:
    @classmethod
    def get_logger(cls, layer_name):
        from loguru import logger
        if layer_name not in [layer.value for layer in LayerNames]:
            return logger

        return logger.bind(layer=layer_name)
