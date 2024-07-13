from typing import Optional
import json

from config import DataAccessError


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
class DatabaseInsertError(DataAccessError):
    def __init__(self, metadata: dict = {}, message: Optional[str] = None):
        base_message = f"Failed to insert into database with row {json.dumps(metadata)}"
        super().__init__(base_message, message)
class DatabaseFetchError(DataAccessError):
    def __init__(self, query: dict = {}, message: Optional[str] = None):
        base_message = f"Failed to fetch from database with query {json.dumps(query)}"
        super().__init__(base_message, message)
class DatabaseUpdateError(DataAccessError):
    def __init__(self, query: dict = {}, update_fields: dict = {}, message: Optional[str] = None):
        base_message = f"Failed to update database record with {json.dumps(query)} and {json.dumps(update_fields)}"
        super().__init__(base_message, message)
class DatabaseDeleteError(DataAccessError):
    def __init__(self, query: dict = {}, message: Optional[str] = None):
        base_message = f"Failed to delete database record with query {json.dumps(query)}"
        super().__init__(base_message, message)

class CacheFetchError(DataAccessError):
    def __init__(self, key: str, message: Optional[str] = None):
        base_message = f"Failed to fetch from cache with key {key}"
        super().__init__(base_message, message)
class CacheInsertError(DataAccessError):
    def __init__(self, key: str, value, message: Optional[str] = None):
        base_message = f"Failed to insert into cache with key {key} and value {value}"
        super().__init__(base_message, message)

class CacheDeleteError(DataAccessError):
    def __init__(self, key: str, message: Optional[str] = None):
        base_message = f"Failed to delete cache record with key {key}"
        super().__init__(base_message, message)

class CacheExpireError(DataAccessError):
    def __init__(self, key: str, ttl: int, message: Optional[str] = None):
        base_message = f"Failed to expire cache record with key {key} and ttl {ttl}"
        super().__init__(base_message, message)
        
class CacheBatchOperationError(DataAccessError):
    def __init__(self, metadata: dict = {}, message: Optional[str] = None):
        base_message = f"Failed to execute batch operation on cache with {json.dumps(metadata)}"
        super().__init__(base_message, message)
        
class CacheFlushError(DataAccessError):
    def __init__(self, message: Optional[str] = None):
        base_message = f"Failed to flush cache"
        super().__init__(base_message, message)
