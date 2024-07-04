import re
from utils.exceptions import PasswordValidationError, PhoneNumberValidationError, EmailValidationError

def validate_password(value: str) -> str:
    if not re.search(r'[A-Z]', value):
        raise PasswordValidationError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', value):
        raise PasswordValidationError('Password must contain at least one lowercase letter')
    if not re.search(r'\d', value):
        raise PasswordValidationError('Password must contain at least one number')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise PasswordValidationError('Password must contain at least one special character')
    return value

def validate_phone_number(value: str) -> str:
    if not re.match(r'^\+\d{1,3}\d{1,14}(?:x\d+)?$', value):
        raise PhoneNumberValidationError('Invalid phone number format')
    return value

def validate_email(value: str) -> str:
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        raise EmailValidationError('Invalid email format')
    return value
