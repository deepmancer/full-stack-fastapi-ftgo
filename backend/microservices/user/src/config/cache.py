from config.base import BaseConfig, env_var

class RedisConfig(BaseConfig):
    container_name: str = env_var("CACHE_CONTAINER_NAME", "user_cache")

    host: str = env_var("REDIS_HOST", "localhost")
    port: int = env_var("REDIS_PORT", 6379, int)
    db: int = env_var("REDIS_DB", 0, int)
    default_ttl: int = env_var("REDIS_DEFAULT_TTL", 120, int)

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"
