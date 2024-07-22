from config.base import BaseConfig, env_var

class RedisConfig(BaseConfig):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: int = None,
        default_ttl: int = None,
    ):
        if host is None:
            config = self.load()
            self.host = config.host
            self.port = config.port
            self.db = config.db
            self.default_ttl = config.default_ttl
        else:
            self.host = host
            self.port = port
            self.db = db
            self.default_ttl = default_ttl
    
    @classmethod
    def load(cls):
        return cls(
            host=env_var("REDIS_HOST", "localhost"),
            port=env_var("REDIS_PORT", 6235, int),
            db=env_var("REDIS_DB", 0, int),
            default_ttl=env_var("REDIS_DEFAULT_TTL", 120, int)
        )

    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"
