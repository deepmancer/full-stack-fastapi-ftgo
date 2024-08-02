from typing import Optional
from pydantic import BaseModel, Field
from ftgo_utils.schemas import (
    uuid_field,
)


class RegisterVehicleRequest(BaseModel):
    plate_number: str = Field(..., min_length=1, max_length=100)
    license_number: str = Field(..., min_length=1, max_length=100)


class RegisterVehicleResponse(BaseModel):
    vehicle_id: str = uuid_field()



class GetVehicleInfoResponse(BaseModel):
    vehicle_id: str = uuid_field()
    driver_id: str = uuid_field()
    plate_number: str = Field(..., min_length=1, max_length=100)
    license_number: str = Field(..., min_length=1, max_length=100)


class DeleteVehicleResponse(BaseModel):
    vehicle_id: str = uuid_field()