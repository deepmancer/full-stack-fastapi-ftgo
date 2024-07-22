import logging
from config.base import BaseConfig, env_var

class ServiceConfig(BaseConfig):
    def __init__(
        self,
        environment: str = None,
        api_prefix: str = None,
        service_host: str = None,
        service_port: int = None,
        log_level_name: str = None,
        debug: bool = None,
    ):
        if service_host is None:
            config = self.load()
            self.environment = config.environment
            self.api_prefix = config.api_prefix
            self.service_host = config.service_host
            self.service_port = config.service_port
            self.log_level_name = config.log_level_name
            self.log_level = config.log_level
            self.debug = config.debug
        else:
            self.environment = environment
            self.api_prefix = api_prefix
            self.service_host = service_host
            self.service_port = service_port
            self.log_level_name = log_level_name
            self.log_level = logging._nameToLevel.get(log_level_name, logging.DEBUG)
            self.debug = debug
        
    @classmethod
    def load(cls):
        return cls(
            environment=env_var('ENVIRONMENT', default='test'),
            api_prefix=env_var('API_PREFIX', default='/api'),
            service_host=env_var('SERVICE_HOST', default='127.0.0.1'),
            service_port=env_var('SERVICE_PORT', default=8000, cast_type=int),
            log_level_name=env_var('LOG_LEVEL', default='INFO'),
            debug=env_var('DEBUG', default=True, cast_type=lambda s: s.lower() in ['true', '1'])
        )
