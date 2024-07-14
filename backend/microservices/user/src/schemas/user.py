
from typing import Optional
from pydantic import Field

from schemas.base import BaseSchema
from schemas.fields import PhoneNumberMixin, RoleMixin, GenderMixin, NationalIdMixin, uuid_field

class UserInfoMixin(PhoneNumberMixin, RoleMixin, GenderMixin, NationalIdMixin):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

class UserMixin(UserInfoMixin):
    user_id: str = uuid_field()
