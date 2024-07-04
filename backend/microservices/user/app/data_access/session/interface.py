# import abstract libs 
from abc import ABC, abstractmethod

class AsyncSessionInterface(ABC):
    @abstractmethod
    async def get_or_create_session(self, *args, **kwargs):
        raise NotImplementedError()
    
    @abstractmethod
    async def connect(self, *args, **kwargs):
        raise NotImplementedError()
    
    @abstractmethod
    async def disconnect(self, *args, **kwargs):
        raise NotImplementedError()
