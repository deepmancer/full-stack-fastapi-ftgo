from config.base import BaseConfig, env_var

class RedisConfig(BaseConfig):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: int = None,
        default_ttl: int = None,
        password: str = None,
    ):
        self.host = host or env_var("REDIS_HOST", "localhost")
        self.port = port or env_var("REDIS_PORT", 6300, int)
        self.db = db or env_var("REDIS_DB", 0, int)
        self.default_ttl = default_ttl or env_var("REDIS_DEFAULT_TTL", 600, int)
        self.password = password or env_var("REDIS_PASSWORD", "location_password")
