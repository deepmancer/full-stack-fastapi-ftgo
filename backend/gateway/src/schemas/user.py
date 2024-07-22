from typing import Optional

from pydantic import Field

from schemas.base import BaseModel

class UserSchema(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    phone_number: str = Field(..., min_length=10, max_length=14)
    role: str = Field(..., min_length=1, max_length=50)
    scope: str = Field(..., min_length=1, max_length=50)
    token: str = Field(..., min_length=1, max_length=255)
