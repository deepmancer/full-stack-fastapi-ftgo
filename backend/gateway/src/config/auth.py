from typing import Optional

from config.base import BaseConfig, env_var


class AuthConfig(BaseConfig):
    def __init__(
        self,
        algorithm: Optional[str] = None,
        access_token_expire_minutes: Optional[int] = None,
        token_location: Optional[list[str]] = None,
        excluded_urls: Optional[list[str]] = None,
        secret: Optional[str] = None,
        cache_key_prefix: Optional[str] = 'session_token_',
    ):
        self.algorithm = algorithm or env_var("AUTH_ALGORITHM", default="HS256")
        self.access_token_expire_minutes = access_token_expire_minutes or env_var("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast_type=int)
        self.token_location = token_location if token_location is not None else env_var("TOKEN_LOCATION", default="headers", cast_type=lambda s: s.split(","))
        self.excluded_urls = excluded_urls if excluded_urls is not None else env_var("EXCLUDED_URLS", default="", cast_type=lambda s: s.split(","))
        self.secret = secret or env_var("TOKEN_SECRET_KEY", default="secret")
        self.cache_key_prefix = cache_key_prefix
