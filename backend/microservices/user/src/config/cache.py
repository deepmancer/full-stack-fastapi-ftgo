from config.base import BaseConfig
from decouple import config as de_config

class RedisConfig(BaseConfig):
    container_name: str = de_config("CACHE_CONTAINER_NAME", default="user_cache")

    host: str = de_config("REDIS_HOST")
    port: int = de_config("REDIS_PORT", cast=int)
    db: int = de_config("REDIS_DB", default=0, cast=int)
    default_ttl: int = de_config("REDIS_DEFAULT_TTL", default=120, cast=int)

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"
