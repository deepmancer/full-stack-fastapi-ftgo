class ValidationError(Exception):
    """Base class for validation errors."""
    pass

class PasswordValidationError(ValidationError):
    """Exception raised for password validation errors."""
    pass

class PhoneNumberValidationError(ValidationError):
    """Exception raised for phone number validation errors."""
    pass

class UserNotFoundError(ValidationError):
    """Exception raised when a user is not found."""
    def __init__(self):
        super().__init__("User not found")

class UserNotVerifiedError(ValidationError):
    """Exception raised when a user is not verified."""
    def __init__(self):
        super().__init__("User is not verified")

class AccountExistsError(ValidationError):
    """Exception raised when an account already exists for a phone number and role."""
    def __init__(self):
        super().__init__("Account already exists for this phone number and role")

class InvalidPasswordError(ValidationError):
    """Exception raised when a password is invalid."""
    def __init__(self):
        super().__init__("Invalid password")

class InvalidAuthenticationCodeError(ValidationError):
    """Exception raised for authentication code errors."""
    def __init__(self, message="Invalid authentication code"):
        super().__init__(message)

class AddressNotFoundError(ValidationError):
    """Exception raised when an address is not found."""
    def __init__(self):
        super().__init__("Address not found")

class DefaultAddressDeletionError(ValidationError):
    """Exception raised when trying to delete a default address."""
    def __init__(self):
        super().__init__("Cannot delete default address")
