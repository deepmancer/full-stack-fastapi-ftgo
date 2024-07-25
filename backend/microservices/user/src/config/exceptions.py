from ftgo_utils.errors import BaseError

from config.enums import LayerNames

class ApplicationError(BaseError):
    scope: str = LayerNames.APP.value

class DomainError(BaseError):
    scope: str = LayerNames.DOMAIN.value

class DataAccessError(BaseError):
    scope: str = LayerNames.DATA_ACCESS.value

class MessageBusError(BaseError):
    scope: str = LayerNames.MESSAGE_BUS.value


def get_error_class(scope: str) -> BaseError:
    if scope == LayerNames.APP.value:
        return ApplicationError
    if scope == LayerNames.DOMAIN.value:
        return DomainError
    if scope == LayerNames.DATA_ACCESS.value:
        return DataAccessError
    if scope == LayerNames.MESSAGE_BUS.value:
        return MessageBusError
    raise ValueError(f"Invalid scope: {scope}")