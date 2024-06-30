from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    email_verified: bool = False
    phone_number_verified: bool = False

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
