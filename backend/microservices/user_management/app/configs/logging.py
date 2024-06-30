import logging
from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

def setup_logging():
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.add("logs/user_microservice.log", rotation="1 MB")
    logger.info("Logging is set up.")

setup_logging()
