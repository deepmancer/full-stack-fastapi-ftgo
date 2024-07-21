from typing import Optional
import json
from config.exceptions import DomainError


class TokenGenerationError(DomainError):
    def __init__(self, user_id, message: Optional[str] = None):
        base_message = f"Token generation failed for User with ID {user_id}"
        super().__init__(base_message, message)

class TokenTTLRetrievalError(DomainError):
    def __init__(self, token: str, message: Optional[str] = None):
        base_message = f"Token TTL retrieval for {token} failed"
        super().__init__(base_message, message)

class TokenValidationError(DomainError):
    def __init__(self, user_id: str, token: str, message: Optional[str] = None):
        base_message = f"Token validation failed for User with ID {user_id} and Token {token}"
        super().__init__(base_message, message)

class AddressNotFoundError(DomainError):
    def __init__(self, address_id: str, message: Optional[str] = None):
        base_message = f"Address with ID {address_id} not found"
        super().__init__(base_message, message)

class UnkownError(DomainError):
    def __init__(self, message: Optional[str] = None):
        base_message = f"An unknown error occurred"
        super().__init__(base_message, message)

class PasswordHashingError(DomainError):
    def __init__(self, password, message: Optional[str] = None):
        base_message = f"Password hashing failed for {password}"
        super().__init__(base_message, message)

class ProfileRegistrationError(DomainError):
    def __init__(self,  message: Optional[str] = None, **kwargs):
        extra_message = f" for {json.dumps(kwargs)}" if kwargs else ""
        base_message = f"Profile registration failed{extra_message}"
        super().__init__(base_message, message)

class ProfileLoginError(DomainError):
    def __init__(self, phone_number: str, role: str, message: Optional[str] = None):
        base_message = f"Profile login failed for phone number {phone_number}, and role {role}"
        super().__init__(base_message, message)

class ProfileDeletionError(DomainError):
    def __init__(self,  user_id: str, message: Optional[str] = None):
        base_message = f"Profile deletion failed for user with ID {user_id}"
        super().__init__(base_message, message)

class ProfileVerificationError(DomainError):
    def __init__(self, user_id: str, auth_code: str, message: Optional[str] = None):
        base_message = f"Profile verification failed for user with ID {user_id} and auth code {auth_code}"
        super().__init__(base_message, message)

class ProfileLogoutError(DomainError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"Profile logout failed for user with ID {user_id}"
        super().__init__(base_message, message)

class UserNotFoundError(DomainError):
    def __init__(self, query: dict, message: Optional[str] = None):
        base_message = f"User not found with query {json.dumps(query)}"
        super().__init__(base_message, message)

class UserNotVerifiedError(DomainError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"User with ID {user_id} is not verified"
        super().__init__(base_message, message)

class AccountExistsError(DomainError):
    def __init__(self, phone_number: str, role: str, message: Optional[str] = None):
        base_message = f"Account with phone number {phone_number} and role {role} already exists"
        super().__init__(base_message, message)

class WrongPasswordError(DomainError):
    def __init__(self, message: Optional[str] = None):
        base_message = "wrong password"
        super().__init__(base_message, message)

class AuthenticationCodeError(DomainError):
    def __init__(self, user_id: str, auth_code: str, message: Optional[str] = None):
        base_message = f"Invalid authentication code {auth_code} for User with ID {user_id}"
        super().__init__(base_message, message)

class WrongAuthenticationCodeError(DomainError):
    def __call__(self, user_id: str, auth_code: str, actual_auth_code: str, message: Optional[str] = None):
        base_message = f"Authentication code {auth_code} does not match actual code {actual_auth_code} for User with ID {user_id}"
        return super().__call__(base_message, message)

class AddressNotFoundError(DomainError):
    def __init__(self, address_id: str, message: Optional[str] = None):
        base_message = f"Address with ID {address_id} not found"
        super().__init__(base_message, message)

class UserAlreadyVerifiedError(DomainError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"User with ID {user_id} is already verified"
        super().__init__(base_message, message)

class DefaultAddressDeletionError(DomainError):
    def __init__(self, address_id: str, message: Optional[str] = None):
        base_message = f"Default address with ID {address_id} cannot be deleted"
        super().__init__(base_message, message)

class UnverifiedSessionError(DomainError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"Session for User with ID {user_id} is not verified"
        super().__init__(base_message, message)

class InvalidTokenWithUserIdError(DomainError):
    def __init__(self, user_id: str, token: str, message: Optional[str] = None):
        base_message = f"Token {token} does not match User with ID {user_id}"
        super().__init__(base_message, message)

class InvalidAuthenticationCodeError(DomainError):
    def __init__(self, message: Optional[str] = None):
        base_message = "Invalid authentication code"
        super().__init__(base_message, message)

class GetAddressError(DomainError):
    def __init__(self, user_id: str, address_id: str, message: Optional[str] = None):
        base_message = f"Failed to get address with ID {address_id} for user with ID {user_id}"
        super().__init__(base_message, message)


class GetAddressInfoError(DomainError):
    def __init__(self, user_id: str, address_id: str, message: Optional[str] = None):
        base_message = f"Failed to get address information with ID {address_id} for user with ID {user_id}"
        super().__init__(base_message, message)

class GetAddressesError(DomainError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"Failed to get addresses for user with ID {user_id}"
        super().__init__(base_message, message)

class AddAddressError(DomainError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"Failed to add address for user with ID {user_id}"
        super().__init__(base_message, message)

class DeleteAddressError(DomainError):
    def __init__(self, user_id: str, address_id: str, message: Optional[str] = None):
        base_message = f"Failed to delete address with ID {address_id} for user with ID {user_id}"
        super().__init__(base_message, message)

class SetDefaultAddressError(DomainError):
    def __init__(self, user_id: str, address_id: str, message: Optional[str] = None):
        base_message = f"Failed to set default address with ID {address_id} for user with ID {user_id}"
        super().__init__(base_message, message)