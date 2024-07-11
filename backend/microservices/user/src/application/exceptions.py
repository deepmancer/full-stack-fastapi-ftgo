from typing import Optional
import json
from config.exceptions import ApplicationError


class DatabaseConnectionError(ApplicationError):
    def __init__(self, url: str, message: Optional[str] = None,):
        base_message = f"Failed to connect to database at {url}"
        super().__init__(base_message, message)
        
class PasswordValidationError(ApplicationError):
    def __init__(self, password: str, message: Optional[str] = None):
        base_message = f"Password {password} is not valid"
        super().__init__(base_message, message)

class InvalidEmailFormatError(ApplicationError):
    def __init__(self, email: str, message: Optional[str] = None):
        base_message = f"Email {email} is not in the correct format"
        super().__init__(base_message, message)
        
class RoleNameError(ApplicationError):
    def __init__(self, role_name: str, message: Optional[str] = None):
        base_message = f"Role name {role_name} is invalid"
        super().__init__(base_message, message)
        
class NationalIdFormatError(ApplicationError):
    def __init__(self, national_id: str, message: Optional[str] = None):
        base_message = f"National ID {national_id} must only contain numbers"
        super().__init__(base_message, message)

class PhoneNumberFormatError(ApplicationError):
    def __init__(self, phone_number: str, message: Optional[str] = None):
        base_message = f"Phone number {phone_number} is not in the correct format"
        super().__init__(base_message, message)

class InvalidUserUUDDError(ApplicationError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"User id {user_id} is not a valid UUID (v4)"
        super().__init__(base_message, message)
