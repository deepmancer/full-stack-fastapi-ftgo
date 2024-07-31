from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dto.base import BaseDTO

@dataclass
class DriverLocationDTO(BaseDTO):
    location_id: Optional[str] = None
    driver_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy: Optional[float] = None
    speed: Optional[float] = None
    bearing: Optional[float] = None
    timestamp: Optional[datetime] = None
