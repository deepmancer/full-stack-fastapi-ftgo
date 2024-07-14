from typing import Optional, List
from pydantic import Field

from schemas import AddressMixin, AddressInfoMixin, BaseSchema, uuid_field

class GetDefaultAddressRequest(BaseSchema):
    user_id: str = uuid_field()

class AddressInfoRequest(BaseSchema):
    user_id: str = uuid_field()
    address_id: str = uuid_field()

class AddressInfoResponse(AddressMixin):
    pass

class AllAddressesRequest(BaseSchema):
    user_id: str = uuid_field()

class AllAddressesResponse(BaseSchema):
    addresses: List[AddressInfoResponse] = Field(...)

class AddAddressRequest(AddressInfoMixin):
    user_id: str = uuid_field()
    address_id: str = uuid_field()
    is_default: Optional[bool] = Field(False)

class AddAddressResponse(AddressMixin):
    success: bool = Field(...)

class DeleteAddressRequest(BaseSchema):
    user_id: str = uuid_field()
    address_id: str = uuid_field()

class DeleteAddressResponse(BaseSchema):
    success: bool = Field(...)
    address_id: str = uuid_field()

class SetPreferredAddressRequest(BaseSchema):
    user_id: str = uuid_field()
    address_id: str = uuid_field()
    set_default: bool = Field(...)

class SetPreferredAddressResponse(BaseSchema):
    success: bool = Field(...)
    address_id: str = uuid_field()
    is_default: bool = Field(...)

class DeleteAllAddressesRequest(BaseSchema):
    success: bool = Field(...)
    user_id: str = uuid_field()

class DeleteAllAddressesResponse(BaseSchema):
    success: bool = Field(...)
    address_ids: List[str] = Field(...)

class UpdateAddressRequest(BaseSchema):
    user_id: str = uuid_field()
    address_id: str = uuid_field()
    address_line_1: Optional[str] = Field(..., min_length=1, max_length=100)
    address_line_2: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)

class UpdateAddressResponse(BaseSchema):
    user_id: str = uuid_field()
    address_id: str = uuid_field()
    address_line_1: Optional[str] = Field(..., min_length=1, max_length=100)
    address_line_2: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(..., min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    success: bool = Field(...)
