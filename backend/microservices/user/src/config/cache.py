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
   
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"
