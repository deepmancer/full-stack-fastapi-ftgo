import enum

class Status(enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class Roles(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPPLIER = "supplier"
    DRIVER = "driver"

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    
class LayerNames(enum.Enum):
    APP = "app"
    DOMAIN = "domain"
    DATA_ACCESS = "data"
