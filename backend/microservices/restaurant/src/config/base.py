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

    @classmethod
    def load_environment(cls):
        env = config("ENVIRONMENT", default='test')
        return env

    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ', '.join(f'{key}={value!r}' for key, value in self.__dict__.items())
        return f'{class_name}({attributes})'

    def dict(self):
        return self.__dict__
