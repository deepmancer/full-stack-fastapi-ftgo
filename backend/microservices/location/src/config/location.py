from config.base import BaseConfig, env_var

class LocationConfig(BaseConfig):
    def __init__(
        self,
        cache_key: str = None,
        cache_ttl: int = None,
        timestamp_maximum_delay_threshold_s: int = None,
        accuracy_threshold_m: int = None,
        maximum_speed_threshold_m: int = None,
        keep_last_locations_count: int = None,
        maximum_location_to_store_per_driver: int = None,
    ):
        self.cache_key = cache_key or env_var("LOCATIONS_CACHE_KEY", default="locations_cache", cast_type=str)
        self.cache_ttl = cache_ttl or env_var("LOCATIONS_CACHE_TTL", default=10 * 60, cast_type=int)
        self.timestamp_maximum_delay_threshold_s = timestamp_maximum_delay_threshold_s or env_var("TIMESTAMP_MAXIMUM_DELAY_THRESHOLD_S", default=5 * 60, cast_type=int)
        self.accuracy_threshold_m = accuracy_threshold_m or env_var("ACCURACY_THRESHOLD_M", default=15, cast_type=int)
        self.maximum_speed_threshold_m = maximum_speed_threshold_m or env_var("MAXIMUM_SPEED_THRESHOLD_M", default=150, cast_type=int)
        self.keep_last_locations_count = keep_last_locations_count or env_var("KEEP_LAST_LOCATIONS_COUNT", default=5, cast_type=int)
        self.maximum_location_to_store_per_driver = maximum_location_to_store_per_driver or env_var("MAXIMUM_LOCATION_TO_STORE_PER_DRIVER", default=20, cast_type=int)
