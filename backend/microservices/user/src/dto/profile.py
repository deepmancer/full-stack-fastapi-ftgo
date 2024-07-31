import email
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from dto.base import BaseDTO

@dataclass
class ProfileDTO(BaseDTO):
    user_id: Optional[str] = None
    phone_number: Optional[str] = None
    hashed_password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[email] = None
    role: Optional[str] = None
    national_id: Optional[str] = None
    verified_at: Optional[datetime] = None
    last_login_time: Optional[datetime] = None
