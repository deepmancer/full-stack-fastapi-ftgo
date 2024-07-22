from typing import Optional
from pydantic import Field

from schemas.base import BaseSchema
from schemas.fields import uuid_field

class AddressInfoMixin(BaseSchema):
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: Optional[str] = Field(None, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)

class AddressMixin(AddressInfoMixin):
    user_id: str = uuid_field()
    address_id: str = uuid_field()
    is_default: Optional[bool] = Field(False)

