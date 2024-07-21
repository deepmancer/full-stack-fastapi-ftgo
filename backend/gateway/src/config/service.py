import logging

from ftgo_utils import class_property

from config.base import BaseConfig, env_var

class ServiceConfig(BaseConfig):
    @class_property
    def environment(cls):
        return env_var('ENVIRONMENT', 'test')

    @class_property
    def api_prefix(cls):
        return env_var('API_PREFIX', '/api')

    @class_property
    def service_host(cls):
        return env_var('SERVICE_HOST', '127.0.0.1')

    @class_property
    def service_port(cls):
        return env_var('SERVICE_PORT', 8000, int)

    @class_property
    def log_level_name(cls):
        return env_var('LOG_LEVEL', 'INFO')
    
    @class_property
    def log_level(cls) -> int:
        return logging._nameToLevel.get(cls.log_level_name, logging.DEBUG)

    @class_property
    def debug(cls):
        return env_var('DEBUG', default=True, cast_type=lambda s: s.lower() in ['true', '1'])
