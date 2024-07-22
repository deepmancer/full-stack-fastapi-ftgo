import logging

from config import BaseConfig, env_var

class ServiceConfig(BaseConfig):
    def __init__(
        self,
        environment: str = None,
        log_level_name: str = None,
    ):
        if environment is None or log_level_name is None:
            config = self.load()
            self.environment = config.environment
            self.log_level_name = config.log_level_name
            self.log_level = config.log_level
        else:
            self.environment = environment
            self.log_level_name = log_level_name
            self.log_level = logging._nameToLevel.get(log_level_name, logging.DEBUG)
        
    @classmethod
    def load(cls):
        return cls(
            environment=env_var('ENVIRONMENT', default='test'),
            log_level_name=env_var('LOG_LEVEL', default='INFO')
        )
