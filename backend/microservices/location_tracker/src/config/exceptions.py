from typing import Optional, Type
from config.enums import LayerNames

class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        self.layer = self.get_layer()
        super().__init__(message)

    def get_layer(self) -> Optional[str]:
        return None
    
    @staticmethod
    def construct_message(base_message: str, context_message: Optional[str]) -> str:
        return base_message + (f": {context_message}" if context_message else "")

    def __str__(self) -> str:
        layer_info = f"layer: {self.layer} | " if self.layer else ""
        cause_info = "\n " + f"Caused by: {self.__cause__}" if self.__cause__ else ""
        return f"{layer_info}{self.message}{cause_info}"

class ApplicationError(BaseError):
    def __init__(self, message: str, context_message: Optional[str] = None):
        super().__init__(self.construct_message(message, context_message))

    def get_layer(self) -> str:
        return LayerNames.APP.value

class DomainError(BaseError):
    def __init__(self, message: str, context_message: Optional[str] = None):
        super().__init__(self.construct_message(message, context_message))

    def get_layer(self) -> str:
        return LayerNames.DOMAIN.value

class DataAccessError(BaseError):
    def __init__(self, message: str, context_message: Optional[str] = None):
        super().__init__(self.construct_message(message, context_message))

    def get_layer(self) -> str:
        return LayerNames.DATA_ACCESS.value
