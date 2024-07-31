from typing import Optional
from pydantic import BaseModel, Field
from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, UserInfoMixin, uuid_field,
)


class AddMenuItemRequest(BaseModel):
    restaurant_id: str = uuid_field()
    name: str = Field(..., min_length=1, max_length=100)
    price: float
    count: int
    description: str = Field(..., min_length=1, max_length=500)


class AddMenuItemResponse(BaseModel):
    item_id: str = uuid_field()


class GetMenuItemInfoRequest(BaseModel):
    item_id: str = uuid_field()
    restaurant_id: str = uuid_field()
    name: str = Field(..., min_length=1, max_length=100)
    price: float
    count: int = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)


class GetMenuItemInfoResponse(BaseModel):
    item_id: str = uuid_field()
    restaurant_id: str = uuid_field()
    name: str = Field(..., min_length=1, max_length=100)
    price: float
    count: int = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)


class UpdateMenuItemRequest(BaseModel):
    item_id: str = uuid_field()
    name: str = Field(..., min_length=1, max_length=100)
    price: float
    count: int = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)


class UpdateMenuItemResponse(BaseModel):
    restaurant_id: str = uuid_field()


class DeleteMenuItemRequest(BaseModel):
    item_id: str = uuid_field()


class DeleteMenuItemResponse(BaseModel):
    item_id: str = uuid_field()


class GetAllMenuItemRequest(BaseModel):
    restaurant_id: str = uuid_field()



class GetAllMenuItemResponse(BaseModel):
    menu: list[GetMenuItemInfoResponse] = Field(...)
