from typing import Optional
from config.base import BaseConfig, env_var

class AuthConfig(BaseConfig):
    def __init__(
        self,
        algorithm: Optional[str] = "HS256",
        access_token_expire_minutes: Optional[int] = 30,
        token_location: Optional[list[str]] = None,
        excluded_urls: Optional[list[str]] = None,
        secret: Optional[str] = None
    ):
        if all(param is None for param in [algorithm, access_token_expire_minutes, token_location, excluded_urls, secret]):
            config = self.load()
            self.algorithm = config.algorithm
            self.access_token_expire_minutes = config.access_token_expire_minutes
            self.token_location = config.token_location
            self.excluded_urls = config.excluded_urls
            self.secret = config.secret
        else:
            self.algorithm = algorithm
            self.access_token_expire_minutes = access_token_expire_minutes
            self.token_location = token_location if token_location is not None else ["headers"]
            self.excluded_urls = excluded_urls if excluded_urls is not None else []
            self.secret = secret
        
    @classmethod
    def load(cls):
        return cls(
            algorithm=env_var("AUTH_ALGORITHM", default="HS256"),
            access_token_expire_minutes=env_var("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast_type=int),
            token_location=env_var("TOKEN_LOCATION", default="headers", cast_type=lambda s: s.split(",")),
            excluded_urls=env_var("EXCLUDED_URLS", default="", cast_type=lambda s: s.split(",")),
            secret=env_var("TOKEN_SECRET_KEY", default="secret")
        )
