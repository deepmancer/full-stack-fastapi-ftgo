from typing import Optional
from pydantic import Field

from schemas import VehicleMixin, VehicleInfoMixin, BaseSchema, uuid_field

class SubmitVehicleRequest(VehicleInfoMixin):
    user_id: str = uuid_field()

class SubmitVehicleResponse(VehicleMixin):
    success: bool = Field(...)

class GetVehicleInfoRequest(BaseSchema):
    user_id: str = uuid_field()

class GetVehicleInfoResponse(VehicleMixin):
    pass
