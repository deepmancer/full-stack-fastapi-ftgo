from typing import Optional
from pydantic import Field, field_validator, ConfigDict, ValidationError
from schemas.base import BaseModel


class TokenSchema(BaseModel):
    token: str

