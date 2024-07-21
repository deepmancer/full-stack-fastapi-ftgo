import os
from typing import Any, Type
from pydantic import Field
from decouple import Config, RepositoryEnv, config
from collections import ChainMap

class BaseConfig():
    @classmethod
    def load_environment(cls):
        common_env_path = ".env"
        env = os.getenv("ENVIRONMENT", "test")
        env_specific_path = f".env.{env}"

        if not os.path.exists(common_env_path):
            raise FileNotFoundError(f"Common environment file {common_env_path} not found.")

        if not os.path.exists(env_specific_path):
            raise FileNotFoundError(f"Environment-specific file {env_specific_path} not found.")
        common_env_params = RepositoryEnv(common_env_path)
        env_specific_params = RepositoryEnv(env_specific_path)
        merged_params = {**common_env_params.data, **env_specific_params.data}
        # for the key-value pairs in the merged_params, set the environment variables
        for key, value in merged_params.items():
            os.environ[key] = value

    @classmethod
    def load(cls):
        cls.load_environment()
        return cls()

def env_var(field_name: str, default: Any, cast_type: Type = str) -> Any:
    return config(field_name, default=default, cast=cast_type)

BaseConfig.load_environment()

