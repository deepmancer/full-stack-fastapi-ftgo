from pydantic import BaseModel, Field
from ftgo_utils.schemas import uuid_field

# Delivery Rating Schemas

class CreateDeliveryRatingRequest(BaseModel):
    delivery_id: str = uuid_field()
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., max_length=500)

class CreateDeliveryRatingResponse(BaseModel):
    rating_id: str = uuid_field()

class UpdateDeliveryRatingRequest(BaseModel):
    rating_id: str = uuid_field()
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., max_length=500)

class UpdateDeliveryRatingResponse(BaseModel):
    rating_id: str = uuid_field()

class GetDeliveryRatingRequest(BaseModel):
    rating_id: str = uuid_field()

class GetDeliveryRatingResponse(BaseModel):
    delivery_id: str = uuid_field()
    rating: int
    comment: str

class GetCustomerDeliveryRatingsRequest(BaseModel):
    pass

class GetCustomerDeliveryRatingsResponse(BaseModel):
    ratings: list[GetDeliveryRatingResponse]

class GetDriverDeliveryRatingsRequest(BaseModel):
    driver_id: str = uuid_field()

class GetDriverDeliveryRatingsResponse(BaseModel):
    ratings: list[GetDeliveryRatingResponse]

# Order Rating Schemas

class CreateOrderRatingRequest(BaseModel):
    order_id: str = uuid_field()
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., max_length=500)

class CreateOrderRatingResponse(BaseModel):
    rating_id: str = uuid_field()

class UpdateOrderRatingRequest(BaseModel):
    rating_id: str = uuid_field()
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., max_length=500)

class UpdateOrderRatingResponse(BaseModel):
    rating_id: str = uuid_field()

class GetOrderRatingRequest(BaseModel):
    rating_id: str = uuid_field()

class GetOrderRatingResponse(BaseModel):
    order_id: str = uuid_field()
    rating: int
    comment: str

class GetCustomerOrderRatingsRequest(BaseModel):
    pass

class GetCustomerOrderRatingsResponse(BaseModel):
    ratings: list[GetOrderRatingResponse]

class GetRestaurantOrderRatingsRequest(BaseModel):
    restaurant_id: str = uuid_field()

class GetRestaurantOrderRatingsResponse(BaseModel):
    ratings: list[GetOrderRatingResponse]
