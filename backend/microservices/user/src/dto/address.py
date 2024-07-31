from typing import Optional
from dataclasses import dataclass

from dto.base import BaseDTO

@dataclass
class AddressDTO(BaseDTO):
    address_id: Optional[str] = None
    user_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = False
