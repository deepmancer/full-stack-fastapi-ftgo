from typing import Optional

from pydantic import Field

from application.schemas.base import BaseModel

class UserSchema(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=36)
    phone_number: str = Field(..., min_length=10, max_length=14)
    hashed_password: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=50)
