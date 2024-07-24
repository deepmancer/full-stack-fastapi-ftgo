import os
from typing import Any, Type, TypeVar, Callable
from pydantic import BaseModel, Field
from decouple import config, UndefinedValueError

T = TypeVar('T')

def env_var(field_name: str, default: Any = None, cast_type: Callable[[str], T] = str) -> T:
    try:
        value = config(field_name, default=default)
        if value is None:
            return default
        return cast_type(value)
    except UndefinedValueError:
        return default
    except (TypeError, ValueError) as e:
        if cast_type is None:
            raise ValueError(f"Failed to cast environment variable {field_name} to {str.__name__}") from e
        else:
            raise ValueError(f"Failed to cast environment variable {field_name} to {cast_type.__name__}") from e

class BaseConfig():
    env = os.getenv("ENVIRONMENT", "test")
    
    @classmethod
    def load_environment(cls):
        env = config("ENVIRONMENT", default='test')
        cls.env = env
        return cls.env
