import asyncio
from typing import Optional, Any
from data_access import get_logger

class BaseDataAccess:
    _config = None
    _instance = None
    _lock = asyncio.Lock()

    async def get_or_create_session(self) -> Any:
        """Create or retrieve a session."""
        raise NotImplementedError()

    async def connect(self, *args, **kwargs) -> None:
        """Establish a connection."""
        raise NotImplementedError()

    async def disconnect(self, *args, **kwargs) -> None:
        """Terminate the connection."""
        raise NotImplementedError()

    @property
    def logger(self):
        return get_logger()

    @classmethod
    def initialize(cls, config: Any) -> "BaseDataAccess":
        """Initialize the data access layer with configuration."""
        cls._config = config

    @classmethod
    async def get_instance(cls) -> "BaseDataAccess":
        """Get the instance of the data access layer, ensuring thread safety."""
        async with cls._lock:
            if cls._instance is None:
                if cls._config is None:
                    raise ValueError(f"{cls.__name__} is not initialized with a config")
                cls._instance = cls(cls._config)
            return cls._instance
