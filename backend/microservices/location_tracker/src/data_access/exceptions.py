from typing import Optional
import json
from config.exceptions import DataAccessError


class DatabaseConnectionError(DataAccessError):
    def __init__(self, url: str, message: Optional[str] = None,):
        base_message = f"Failed to connect to database at {url}"
        super().__init__(base_message, message)

class CacheConnectionError(DataAccessError):
    def __init__(self, url: str, message: Optional[str] = None,):
        base_message = f"Failed to connect to cache at {url}"
        super().__init__(base_message, message)

class DatabaseTransactionError(DataAccessError):
    def __init__(self, metadata: dict = {}, message: Optional[str] = None):
        base_message = f"Failed to execute database transaction with {json.dumps(metadata)}"
        super().__init__(base_message, message)
        
class CacheTransactionError(DataAccessError):
    def __init__(self, metadata: dict = {}, message: Optional[str] = None):
        base_message = f"Failed to execute cache transaction with {json.dumps(metadata)}"
        super().__init__(base_message, message)

class DatabaseSessionCreationError(DataAccessError):
    def __init__(self, message: Optional[str] = None):
        base_message = f"Failed to create database session"
        super().__init__(base_message, message)

class CacheSessionCreationError(DataAccessError):
    def __init__(self, message: Optional[str] = None):
        base_message = f"Failed to create cache session"
        super().__init__(base_message, message)
