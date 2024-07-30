from config.enums import LayerNames

class LoggerFactory:
    @classmethod
    def get_logger(cls, layer):
        from loguru import logger
        if layer not in [layer.value for layer in LayerNames]:
            return logger

        return logger.bind(layer=layer)
