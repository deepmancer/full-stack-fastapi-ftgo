from typing import Optional
from dataclasses import dataclass

from dto.base import BaseDTO

@dataclass
class VehicleDTO(BaseDTO):
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    plate_number: Optional[str] = None
    license_number: Optional[str] = None
