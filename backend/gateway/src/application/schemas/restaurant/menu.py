from typing import Optional
from pydantic import BaseModel, Field
from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, UserInfoMixin, uuid_field,
)

class AddMenuItemResponse(BaseModel):
    restaurant_id: str = uuid_field()

class GetMenuItemInfoResponse(BaseModel):
    restaurant_id: str = uuid_field()

class UpdateMenuItemResponse(BaseModel):
    restaurant_id: str = uuid_field()

class DeleteMenuItemResponse(BaseModel):
    restaurant_id: str = uuid_field()