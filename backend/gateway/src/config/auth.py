from typing import Optional 

from config.base import BaseConfig, env_var

from ftgo_utils import class_property

class AuthConfig(BaseConfig):
    algorithm: Optional[str] = "HS256"
    access_token_expire_minutes: Optional[int] = 30
    token_location: Optional[list[str]] = ["headers"]
    excluded_urls: Optional[list[str]] = []

    @class_property
    def secret(cls) -> Optional[str]:
        return env_var("TOKEN_SECRET_KEY", default="secret")
