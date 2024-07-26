from typing import Optional
from pydantic import BaseModel, Field
from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, UserInfoMixin, uuid_field,
)

class AddressInfoResponse(BaseModel):
    address_id: str
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    is_default: bool = Field(...)

class AllAddressesResponse(BaseModel):
    addresses: list[AddressInfoResponse] = Field(...)


class AddAddressRequest(BaseModel):
    address_line_1: str = Field(..., min_length=1, max_length=100)
    address_line_2: str = Field(..., max_length=100)
    city: str = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)

class AddAddressResponse(BaseModel):
    address_id: Optional[str] = Field(None, min_length=1, max_length=36)


class DeleteAddressRequest(BaseModel):
    address_id: Optional[str] = Field(None, min_length=1, max_length=36)
class DeleteAddressResponse(BaseModel):
    address_id: Optional[str] = Field(None, min_length=1, max_length=36)


class SetPreferredAddressRequest(BaseModel):
    address_id: Optional[str] = Field(None, min_length=1, max_length=36)
class SetPreferredAddressResponse(BaseModel):
    address_id: Optional[str] = Field(None, min_length=1, max_length=36)

