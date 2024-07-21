import logging
from config.base import BaseConfig, env_var

class ServiceConfig(BaseConfig):
    api_prefix: str = env_var('API_PREFIX', '/user')
    service_host: str = env_var('SERVICE_HOST', '127.0.0.1')
    service_port: int = env_var('SERVICE_PORT', 5025, int)
    log_level_name: str = env_var('LOG_LEVEL', 'INFO')
    
    @property
    def log_level(self) -> int:
        level = logging._nameToLevel.get(self.log_level_name, logging.DEBUG)
        return level
