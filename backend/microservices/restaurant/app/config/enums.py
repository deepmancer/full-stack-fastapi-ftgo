from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"
