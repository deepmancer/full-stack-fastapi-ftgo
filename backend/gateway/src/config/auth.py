from config.base import BaseConfig
from typing import Optional 
from decouple import config as de_config

class AuthConfig(BaseConfig):
    algorithm: Optional[str] = "HS256"
    access_token_expire_minutes: Optional[int] = 30
    secret: Optional[str] = de_config("TOKEN_SECRET_KEY")
    token_location: Optional[list[str]] = ["headers"]
    excluded_urls: Optional[list[str]] = []
