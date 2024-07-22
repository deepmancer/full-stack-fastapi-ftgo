import os
from typing import Any, Type, TypeVar
from pydantic import BaseModel, Field
from decouple import Config, RepositoryEnv, config
from collections import ChainMap

T = TypeVar('T')

def env_var(field_name: str, default = None, cast_type = str) -> T:
    try:
        value = config(field_name, default=default)
        return cast_type(value)
    except Exception:
        return default

class BaseConfig():
    env = os.getenv("ENVIRONMENT", "test")
    
    @classmethod
    def load_environment(cls):
        env = config("ENVIRONMENT", default=cls.env)
        cls.env = env
        return cls.env

    @classmethod
    def load_var(cls, variable_name: str):
        return os.getenv(variable_name, None)

    @classmethod
    def load_environment(cls):
        common_env_path = ".env"

        env = os.getenv("ENVIRONMENT", "test")
        cls.env = env
        
        env_specific_path = f".env.{env}"

        if not os.path.exists(common_env_path):
            raise FileNotFoundError(f"Common environment file {common_env_path} not found.")

        if not os.path.exists(env_specific_path):
            raise FileNotFoundError(f"Environment-specific file {env_specific_path} not found.")
        common_env_params = RepositoryEnv(common_env_path)
        env_specific_params = RepositoryEnv(env_specific_path)
        merged_params = {**common_env_params.data, **env_specific_params.data}
        for key, value in merged_params.items():
            os.environ[key] = value

    @classmethod
    def load(cls):
        cls.load_environment()
        return cls()
