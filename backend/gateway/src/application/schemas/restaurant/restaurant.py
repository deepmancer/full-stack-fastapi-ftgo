from typing import Optional
from pydantic import BaseModel, Field
from ftgo_utils.schemas import (
    PhoneNumberMixin, RoleMixin, UserMixin, UserInfoMixin, uuid_field,
)


class RegisterRestaurantRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=300)
    address_lat: float
    address_lng: float
    restaurant_licence_id: str = Field(..., min_length=1, max_length=100)


class RegisterRestaurantResponse(BaseModel):
    restaurant_id: str = uuid_field()


class GetRestaurantInfoResponse(BaseModel):
    id: str = uuid_field()
    owner_user_id: str = uuid_field()
    name: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=300)
    address_lat: float
    address_lng: float
    restaurant_licence_id: str = Field(..., min_length=1, max_length=100)


class GetAllRestaurantInfoResponse(BaseModel):
    restaurants: list[GetRestaurantInfoResponse] = Field(...)


class DeleteRestaurantRequest(BaseModel):
    restaurant_id: str = uuid_field()


class DeleteRestaurantResponse(BaseModel):
    restaurant_id: str = uuid_field()


class UpdateRestaurantRequest(BaseModel):
    restaurant_id: str = uuid_field()
    name: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=300)
    address_lat: float
    address_lng: float


class UpdateRestaurantResponse(BaseModel):
    restaurant_id: str = uuid_field()