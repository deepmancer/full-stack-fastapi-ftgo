import enum

class Roles(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    RESTAURANT = "restaurant"
    DRIVER = "driver"

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    
class LayerNames(enum.Enum):
    APP = "app"
    DOMAIN = "domain"
    DATA_ACCESS = "data"
