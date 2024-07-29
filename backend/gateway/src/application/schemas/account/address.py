from typing import Optional

from pydantic import Field

from ftgo_utils.schemas import (
    uuid_field,
    AddressMixin,
    BaseSchema,
)


class AddressesSchema(BaseSchema):
    addresses: list[AddressMixin] = Field(...)

class AddressIdSchema(BaseSchema):
    address_id: str = uuid_field()

class AddressIdPreferencySchema(AddressIdSchema):
    is_default: Optional[bool] = Field(False)
