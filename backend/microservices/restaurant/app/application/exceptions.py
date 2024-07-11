from typing import Optional
from config.exceptions import ApplicationError

class RestaurantNotFoundError(ApplicationError):
    def __init__(self, restaurant_id: str, message: Optional[str] = None):
        base_message = f"Restaurant with ID {restaurant_id} not found"
        super().__init__(base_message, message)

class DuplicateRestaurantError(ApplicationError):
    def __init__(self, restaurant_name: str, message: Optional[str] = None):
        base_message = f"Restaurant with name {restaurant_name} already exists"
        super().__init__(base_message, message)

class InvalidRestaurantEmailError(ApplicationError):
    def __init__(self, email: str, message: Optional[str] = None):
        base_message = f"Email {email} is not in the correct format"
        super().__init__(base_message, message)

class InvalidRestaurantPhoneNumberError(ApplicationError):
    def __init__(self, phone_number: str, message: Optional[str] = None):
        base_message = f"Phone number {phone_number} is not in the correct format"
        super().__init__(base_message, message)

class InvalidRestaurantUUIDError(ApplicationError):
    def __init__(self, restaurant_id: str, message: Optional[str] = None):
        base_message = f"Restaurant ID {restaurant_id} is not a valid UUID"
        super().__init__(base_message, message)
