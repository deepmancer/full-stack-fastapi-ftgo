import enum

class Roles(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    RESTAURANT_ADMIN = "restaurant_admin"
    DRIVER = "driver"
    STAFF = "staff"

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    
class LayerNames(enum.Enum):
    GATEWAY = "gateway"
    DATA_ACCESS = "data"
    EVENT = "event"

class Scopes(enum.Enum):
    SUPER_USER = "superuser"
    ADMIN = "admin"
    USER = "user"
    RESTAURANT = "restaurant"
    DRIVER = "driver"
    CUSTOMER = "customer"
