from typing import Optional
import json
from config.exceptions import DomainError
class RestaurantExistsError(DomainError):
    def __init__(self, phone_number, message: Optional[str] = None):
        base_message = f"The restaurant already exist for the Phone Number {phone_number}"
        super().__init__(base_message, message)

class MenuCreationError(DomainError):
    def __init__(self, restaurant_id: str, message: Optional[str] = None):
        base_message = f"The menu creation have been failed for restaurant_id {restaurant_id}"
        super().__init__(base_message, message)

class MenuItemError(DomainError):
    def __init__(self, restaurant_id: str, item_id: str, message: Optional[str] = None):
        base_message = f"The menu modifying have been failed for restaurant_id {restaurant_id} and item_id {item_id}"
        super().__init__(base_message, message)

class OrderError(DomainError):
    def __init__(self, restaurant_id: str, message: Optional[str] = None):
        base_message = f"The order have been failed for restaurant_id {restaurant_id}"
        super().__init__(base_message, message)

class RestaurantNotFoundError(DomainError):
    def __init__(self, restaurant_id: str, message: Optional[str] = None):
        base_message = f"Restaurant not found with restaurant_id {restaurant_id}"
        super().__init__(base_message, message)
