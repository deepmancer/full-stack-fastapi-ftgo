from pydantic import BaseModel, Field
from typing import Optional, List

class LocationSchema(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: float = Field(..., ge=0)
    accuracy: Optional[float] = Field(None, ge=0)
    speed: Optional[float] = Field(None, ge=0)
    bearing: Optional[float] = Field(None, ge=0, le=360)

class IndexedLocationSchema(LocationSchema):
    h3_index: str = Field(...)
    timestamp: float = Field(..., ge=0)
