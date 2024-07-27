import logging
from config import BaseConfig, env_var

class ServiceConfig(BaseConfig):
    def __init__(
        self,
        environment: str = None,
        log_level_name: str = None,
    ):
        self.environment = environment or env_var('ENVIRONMENT', default='test')
        self.log_level_name = log_level_name or env_var('LOG_LEVEL', default='INFO')
        self.log_level = logging._nameToLevel.get(self.log_level_name, logging.DEBUG)
