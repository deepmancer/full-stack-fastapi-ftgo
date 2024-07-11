from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from application.validators import (
    validate_uuid, validate_email, validate_phone_number,
    validate_password
)
from config.enums import OrderStatus


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, populate_by_name=True)


class RegisterRestaurantRequest(BaseSchema):
    name: str = Field(..., min_length=3, max_length=50)
    owner_name: str = Field(..., min_length=3, max_length=50)
    address: str = Field(..., min_length=10, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=14)
    email: Optional[str] = Field(None, max_length=50)
    password: str = Field(..., min_length=8, max_length=30)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('email', mode='before')
    def validate_email_field(cls, value):
        return validate_email(value)

    @field_validator('password', mode='before')
    def validate_password_field(cls, value):
        return validate_password(value)


class RegisterRestaurantResponse(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)


class AddMenuItemRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    price: float = Field(..., gt=0)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)


class AddMenuItemResponse(BaseSchema):
    menu_item_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('menu_item_id', mode='before')
    def validate_menu_item_id_field(cls, value):
        return validate_uuid(value)


class UpdateMenuItemRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)
    menu_item_id: str = Field(..., min_length=1, max_length=36)
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    price: Optional[float] = Field(None, gt=0)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('menu_item_id', mode='before')
    def validate_menu_item_id_field(cls, value):
        return validate_uuid(value)


class UpdateMenuItemResponse(BaseSchema):
    menu_item_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('menu_item_id', mode='before')
    def validate_menu_item_id_field(cls, value):
        return validate_uuid(value)


class DeleteMenuItemRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)
    menu_item_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('menu_item_id', mode='before')
    def validate_menu_item_id_field(cls, value):
        return validate_uuid(value)


class DeleteMenuItemResponse(BaseSchema):
    menu_item_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('menu_item_id', mode='before')
    def validate_menu_item_id_field(cls, value):
        return validate_uuid(value)


class GetMenuRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)


class MenuItemSchema(BaseSchema):
    menu_item_id: str = Field(..., min_length=1, max_length=36)
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    price: float = Field(..., gt=0)

    @field_validator('menu_item_id', mode='before')
    def validate_menu_item_id_field(cls, value):
        return validate_uuid(value)


class GetMenuResponse(BaseSchema):
    menu_items: List[MenuItemSchema]


class ReceiveOrderRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)
    customer_id: str = Field(..., min_length=1, max_length=36)
    order_items: List[str] = Field(..., min_length=1)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('customer_id', mode='before')
    def validate_customer_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('order_items', mode='before')
    def validate_order_items_field(cls, value):
        return [validate_uuid(item) for item in value]


class ReceiveOrderResponse(BaseSchema):
    order_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('order_id', mode='before')
    def validate_order_id_field(cls, value):
        return validate_uuid(value)


class UpdateOrderStatusRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)
    order_id: str = Field(..., min_length=1, max_length=36)
    status: OrderStatus = Field(...)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('order_id', mode='before')
    def validate_order_id_field(cls, value):
        return validate_uuid(value)


class UpdateOrderStatusResponse(BaseSchema):
    order_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('order_id', mode='before')
    def validate_order_id_field(cls, value):
        return validate_uuid(value)


class GetOrdersRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)


class OrderSchema(BaseSchema):
    order_id: str = Field(..., min_length=1, max_length=36)
    customer_id: str = Field(..., min_length=1, max_length=36)
    order_items: List[str] = Field(..., min_length=1)
    status: OrderStatus = Field(...)

    @field_validator('order_id', mode='before')
    def validate_order_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('customer_id', mode='before')
    def validate_customer_id_field(cls, value):
        return validate_uuid(value)


class GetOrdersResponse(BaseSchema):
    orders: List[OrderSchema]


class GetRestaurantInfoRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)


class GetRestaurantInfoResponse(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)
    name: str = Field(..., min_length=3, max_length=50)
    owner_name: str = Field(..., min_length=3, max_length=50)
    address: str = Field(..., min_length=10, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=14)
    email: Optional[str] = Field(None, max_length=50)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('email', mode='before')
    def validate_email_field(cls, value):
        return validate_email(value)


class UpdateRestaurantInfoRequest(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    owner_name: Optional[str] = Field(None, min_length=3, max_length=50)
    address: Optional[str] = Field(None, min_length=10, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=14)
    email: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=30)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)

    @field_validator('email', mode='before')
    def validate_email_field(cls, value):
        return validate_email(value)

    @field_validator('password', mode='before')
    def validate_password_field(cls, value):
        return validate_password(value)


class UpdateRestaurantInfoResponse(BaseSchema):
    restaurant_id: str = Field(..., min_length=1, max_length=36)

    @field_validator('restaurant_id', mode='before')
    def validate_restaurant_id_field(cls, value):
        return validate_uuid(value)
