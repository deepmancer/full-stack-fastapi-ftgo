from token import OP
from typing import Optional

from pydantic import Field

from ftgo_utils.schemas import uuid_field, RoleMixin, PhoneNumberMixin, UserIdMixin

class UserStateSchema(PhoneNumberMixin, RoleMixin, UserIdMixin):
    #TODO fix role max_length in fgto_utils
    role: str = Field(..., min_length=1, max_length=20)
    hashed_password: str = Field(..., min_length=1, max_length=512)
    token: Optional[str] = Field(None, min_length=1, max_length=1024)
