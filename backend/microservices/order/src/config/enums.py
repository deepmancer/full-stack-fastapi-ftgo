import enum

class LayerNames(str, enum.Enum):
    APP = "app"
    DOMAIN = "domain"
    DATA_ACCESS = "data_access"
    MESSAGE_BROKER = "message_broker"
