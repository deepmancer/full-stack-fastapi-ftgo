import os
from typing import Any, Type
from pydantic import Field
from pydantic_settings import BaseSettings

from dotenv import load_dotenv, find_dotenv

class BaseConfig(BaseSettings):
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "dev"))

    @staticmethod
    def load_common_env():
        common_env = find_dotenv(".env")
        if common_env:
            load_dotenv(common_env)
        else:
            raise FileNotFoundError("Common environment file .env not found.")

    @staticmethod
    def load_env_specific():
        env = os.getenv("ENVIRONMENT", "development")
        env_file = f".env.{env}"
        specific_env = find_dotenv(env_file)
        if specific_env:
            load_dotenv(specific_env, override=True)
        else:
            raise FileNotFoundError(f"Environment-specific file {env_file} not found.")

    @classmethod
    def load(cls):
        cls.load_common_env()
        cls.load_env_specific()
        return cls()

def env_var(field_name: str, default: Any, cast_type: Type = str) -> Any:
    return Field(default_factory=lambda: cast_type(os.getenv(field_name, default)))
