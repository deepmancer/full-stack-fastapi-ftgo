from config.base import BaseConfig, env_var

class HexagonConfig(BaseConfig):
    def __init__(
        self,
        cache_key: str = None,
        cache_ttl: int = None,
        driver_hexagon_cache_key: str = None,
        driver_hexagon_cache_ttl: int = None,
        hexagon_resolution: int = None,
        k_ring_radius: int = None,
    ):
        self.cache_key = cache_key or env_var("HEXAGONS_CACHE_KEY", default="hexagons_cache", cast_type=str)
        self.cache_ttl = cache_ttl or env_var("HEXAGONS_CACHE_TTL", default=10 * 60, cast_type=int)
        self.driver_hexagon_cache_key = driver_hexagon_cache_key or env_var("DRIVER_HEXAGON_CACHE_KEY", default="driver_hexagon_cache", cast_type=str)
        self.driver_hexagon_cache_ttl = driver_hexagon_cache_ttl or env_var("DRIVER_HEXAGON_CACHE_TTL", default=10 * 60, cast_type=int)
        self.hexagon_resolution = hexagon_resolution or env_var("HEXAGON_RESOLUTION", default=8, cast_type=int)
        self.k_ring_radius = k_ring_radius or env_var("K_RING_RADIUS", default=1, cast_type=int)
