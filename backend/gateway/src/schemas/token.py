from typing import Optional
from pydantic import Field, field_validator, ConfigDict, ValidationError
from utils.validators import validate_password, validate_phone_number, validate_role, validate_uuid
from schemas.base import BaseModel


class TokenSchema(BaseModel):
    token: str

