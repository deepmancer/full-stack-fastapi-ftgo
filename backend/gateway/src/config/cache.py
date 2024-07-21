from ftgo_utils import class_property

from config.base import BaseConfig, env_var

class RedisConfig(BaseConfig):
    @class_property
    def host(cls):
        return env_var("REDIS_HOST", "localhost")
    @class_property
    def port(cls):
        return env_var("REDIS_PORT", 6940, int)
    @class_property
    def db(cls):
        return env_var("REDIS_DB", 0, int)
    @class_property
    def default_ttl(cls):
        return env_var("REDIS_DEFAULT_TTL", 600, int)

    @class_property
    def url(cls) -> str:
        return f"redis://{cls.host}:{cls.port}/{cls.db}"
