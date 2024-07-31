from config.base import BaseConfig, env_var

class DriverStatusConfig(BaseConfig):
    def __init__(
        self,
        cache_key: str = None,
        persistent_ttl: int = None,
    ):
        self.cache_key = cache_key or env_var("DRIVER_STATUS_CACHE_KEY", default="driver_status", cast_type=str)
        self.cache_ttl = persistent_ttl or env_var("DRIVER_STATUS_CACHE_TTL", default=600, cast_type=int)
