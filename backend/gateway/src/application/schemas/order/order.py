from typing import Optional, Any

from pydantic import Field

from ftgo_utils.schemas import (
    uuid_field,
    AddressMixin,
    BaseSchema,
)


class CreateOrderRequest(BaseSchema):
    restaurant_id: str = uuid_field()
    items: list[dict[str, Any]]


class GetOrderHistoryRequest(BaseSchema):
    order_id: str = uuid_field()


class GetOrderHistoryResponse(BaseSchema):
    customer_id: str = uuid_field()
    restaurant_id: str = uuid_field()
    total_amount: float = Field(..., gt=0)
    order_items: list[dict[str, Any]]
    status_history: list


class UpdateOrderRequest(BaseSchema):
    items: list[dict[str, Any]]
    status_history: list
    total_amount: float = Field(..., gt=0)


class ConfirmOrderRequest(BaseSchema):
    order_id: str = uuid_field()
    restaurant_id: str = uuid_field()


class RejectOrderRequest(BaseSchema):
    order_id: str = uuid_field()
    restaurant_id: str = uuid_field()