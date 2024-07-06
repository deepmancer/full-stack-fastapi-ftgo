import enum

class Roles(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPPLIER = "supplier"
    DRIVER = "driver"

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
