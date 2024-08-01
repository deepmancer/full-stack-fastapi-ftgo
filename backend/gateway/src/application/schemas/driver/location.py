from typing import Optional, List

from pydantic import Field

from ftgo_utils.schemas import LocationMixin, BaseSchema, LocationPointMixin

class LocationsSchema(BaseSchema):
    locations: List[LocationMixin] = Field(..., min_items=1)
