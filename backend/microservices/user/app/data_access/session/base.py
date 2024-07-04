from abc import ABC, abstractmethod
import asyncio
from typing import Optional, Any, AsyncGenerator

from configs.base import BaseConfig

class BaseDataAccess(ABC):
    _config = Optional[BaseConfig] = None
    _instance: Optional["BaseDataAccess"] = None
    _lock = asyncio.Lock()

    @abstractmethod
    async def get_or_create_session(self, *args, **kwargs) -> Any:
        """Create or retrieve a session."""
        raise NotImplementedError()

    @abstractmethod
    async def connect(self, *args, **kwargs) -> None:
        """Establish a connection."""
        raise NotImplementedError()

    @abstractmethod
    async def disconnect(self, *args, **kwargs) -> None:
        """Terminate the connection."""
        raise NotImplementedError()

    @classmethod
    def initialize(cls, config: Any) -> "BaseDataAccess":
        """Initialize the data access layer with configuration."""
        cls._config = config
        if not cls._instance:
            cls._instance = cls(config)
        return cls._instance

    @classmethod
    async def get_instance(cls) -> "BaseDataAccess":
        """Get the instance of the data access layer, ensuring thread safety."""
        async with cls._lock:
            if cls._instance is None:
                if cls._config is None:
                    raise ValueError(f"{cls.__name__} is not initialized with a config")
                cls._instance = cls(cls._config)
            return cls._instance
