import enum

class LayerNames(str, enum.Enum):
    GATEWAY = "gateway"
    DOMAIN = "domain"
    DATA_ACCESS = "data_access"
    MESSAGE_BROKER = "message_broker"
    MIDDLEWARE = "middleware"
