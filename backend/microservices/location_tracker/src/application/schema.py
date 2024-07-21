from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from ftgo_utils.enums import Roles
from typing import Optional, List
from application.validators import validate_timestamp, validate_speed, validate_accuracy, validate_uuid, validate_status


class BaseSchema(BaseModel):    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, populate_by_name=True)

class LocationSchema(BaseSchema):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: float = Field(..., ge=0)
    accuracy: Optional[float] = Field(None, ge=0)
    speed: Optional[float] = Field(None, ge=0)
    bearing: Optional[float] = Field(None, ge=0, le=360)

    @field_validator('timestamp', mode='before')
    def validate_timestamp_field(cls, value):
        return validate_timestamp(value)
        
    @field_validator('speed', mode='before')
    def validate_speed_field(cls, value):
        return validate_speed(value)
    
    @field_validator('accuracy', mode='before')
    def validate_accuracy_field(cls, value):
        return validate_accuracy(value)

class DriverLocationSchema(BaseSchema):
    driver_id: str = Field(..., min_length=1, max_length=36)
    location: LocationSchema = Field(...)
    timestamp: float = Field(..., ge=0)
    
    @field_validator('driver_id', mode='before')
    def validate_driver_id_field(cls, value):
        return validate_uuid(value)
    
    @field_validator('timestamp', mode='before')
    def validate_timestamp_field(cls, value):
        return validate_timestamp(value)

class SubmitLocationRequest(BaseSchema):
    driver_id: str = Field(..., min_length=1, max_length=36)
    location: List[LocationSchem] = Field(...)
    timestamp: float = Field(..., ge=0)
    
    @field_validator('driver_id', mode='before')
    def validate_driver_id_field(cls, value):
        return validate_uuid(value)
    
    @field_validator('timestamp', mode='before')
    def validate_timestamp_field(cls, value):
        return validate_timestamp(value)

class SubmitLocationResponse(BaseSchema):
    success: bool = Field(...)

class ChangeStatusRequest(BaseSchema):
    driver_id: str = Field(..., min_length=1, max_length=36)
    status: str = Field(..., min_length=1, max_length=10)
    timestamp: float = Field(..., ge=0)
    
    @field_validator('driver_id', mode='before')
    def validate_driver_id_field(cls, value):
        return validate_uuid(value)
    
    @field_validator('timestamp', mode='before')
    def validate_timestamp_field(cls, value):
        return validate_timestamp(value)
    
    @field_validator('status', mode='before')
    def validate_status_field(cls, value):
        return validate_status(value)

class ChangeStatusResponse(BaseSchema):
    success: bool = Field(...)

class GetNearestDriversRequest(BaseSchema):
    location: LocationSchema = Field(...)
    radius: int = Field(..., ge=0)
    max_count: int = Field(..., ge=0)

class GetNearestDriversResponse(BaseSchema):
    driver_locations: List[DriverLocationSchema] = Field(...)
