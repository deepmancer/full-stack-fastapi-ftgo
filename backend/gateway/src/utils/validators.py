import uuid
import string
import validators
from pydantic import ValidationError
from config.enums import Roles, Gender


def validate_uuid(user_id: str):
    return user_id
    if not user_id:
        raise Exception
    user_id = user_id.strip()
    user_uuid = uuid.UUID(user_id, version=4)
    return user_id


def validate_email(email: str):
    if not email:
        return email
    email = email.strip()
    if validators.email(email):
        return email
    raise Exception


def validate_role(role: str):
    role = role.strip()
    eligible_roles = [field.value for field in Roles]
    if role not in eligible_roles:
        raise ValueError(f"Invalid role name {role}, must be one of {eligible_roles}")
    return role

def validate_phone_number(phone_number: str):
    phone_number = phone_number.strip().replace(" ", "")
    if phone_number.startswith("+98"):
        phone_number = phone_number[3:]
    elif phone_number.startswith("98"):
        phone_number = phone_number[2:]
        
    if phone_number.startswith("09"):
        phone_number = phone_number[1:]
    elif phone_number.startswith("9"):
        pass
    else:
        raise ValueError("Invalid phone number format")
    
    if not phone_number.isdigit():
        raise ValueError("Phone number should only contain numbers")
    
    if len(phone_number) != 10:
        raise ValueError("Phone number should be 10 digits long")
    
    return phone_number

def validate_password(password: str):
    if not password:
        raise ValueError("Password cannot be empty")
    
    if len(password) < 8:
        raise ValueError("Password should be at least 8 characters long")
    
    if not any(char.isdigit() for char in password):
        raise ValueError("Password should contain at least one digit")
    
    if not any(char.isupper() for char in password):
        raise ValueError("Password should contain at least one uppercase letter")
    
    if not any(char.islower() for char in password):
        raise ValueError("Password should contain at least one lowercase letter")
    
    if not any(char in string.punctuation for char in password):
        raise ValueError("Password should contain at least one special character")

    return password
