# application/validators.py

import re
import uuid
from application.exceptions import ValidationError
from config.enums import Role

def validate_uuid(value: str) -> str:
    try:
        uuid.UUID(value)
    except ValueError:
        raise ValidationError(f"Invalid UUID: {value}")
    return value

def validate_email(value: str) -> str:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError(f"Invalid email address: {value}")
    return value

def validate_phone_number(value: str) -> str:
    phone_regex = r'^\+?[1-9]\d{1,14}$'
    if not re.match(phone_regex, value):
        raise ValidationError(f"Invalid phone number: {value}")
    return value

def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    return value

def validate_role(value: str) -> str:
    if value not in Role._member_names_:
        raise ValidationError(f"Invalid role: {value}")
    return value
