import logging

from config.base import BaseConfig, env_var


class ServiceConfig(BaseConfig):
    def __init__(
        self,
        environment: str = None,
        api_prefix: str = None,
        simulator_api_prefix: str = None,
        service_host: str = None,
        service_port: int = None,
        log_level_name: str = None,
        debug: bool = None,
    ):
        self.environment = environment or env_var('ENVIRONMENT', default='test')
        self.api_prefix = api_prefix or env_var('API_PREFIX', default='/api/v1')
        self.simulator_api_prefix = simulator_api_prefix or env_var('SIMULATOR_API_PREFIX', default='/simulator/v1')
        self.service_host = service_host or env_var('SERVICE_HOST', default='0.0.0.0')
        self.service_port = service_port or env_var('SERVICE_PORT', default=8000, cast_type=int)
        self.log_level_name = log_level_name or env_var('LOG_LEVEL', default='INFO')
        self.log_level = logging._nameToLevel.get(self.log_level_name, logging.DEBUG)
        self.debug = debug if debug is not None else env_var('DEBUG', default=True, cast_type=lambda s: s.lower() in ['true', '1'])
