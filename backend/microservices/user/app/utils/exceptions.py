class ValidationError(Exception):
    """Base class for validation errors."""
    pass

class PasswordValidationError(ValidationError):
    """Exception raised for password validation errors."""
    pass

class PhoneNumberValidationError(ValidationError):
    """Exception raised for phone number validation errors."""
    pass