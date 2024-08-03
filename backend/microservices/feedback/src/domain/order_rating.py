from typing import List, Optional, Any, Dict
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger
from domain.entities.order_rating import OrderRating
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger
from typing import Dict, Any
from ftgo_utils.enums import DeliveryStatus
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger
from models import DeliveryRating as DeliveryRatingModel
from models import OrderRating as OrderRatingModel
from utils import handle_exception
from domain.entities.delivery_rating import DeliveryRating
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger

class OrderRatingHandler:
    @staticmethod
    async def create_order_rating(order_id: str, customer_id: str, rating: int, feedback: Optional[str] = None) -> OrderRating:
        try:
            order_rating = OrderRating.create(order_id=order_id, customer_id=customer_id, rating=rating, feedback=feedback)
            await order_rating.save()
            return order_rating
        except Exception as e:
            payload = {"order_id": order_id, "customer_id": customer_id}
            get_logger().error(ErrorCodes.CREATE_ORDER_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.CREATE_ORDER_RATING_ERROR, payload=payload) from e

    @staticmethod
    async def update_order_rating(order_id: str, customer_id: str, rating: int, feedback: Optional[str] = None):
        try:
            order_rating = await OrderRating.load(order_id=order_id, customer_id=customer_id)
            if not order_rating:
                raise BaseError(error_code=ErrorCodes.ORDER_RATING_NOT_FOUND_ERROR, payload={"order_id": order_id})
            await order_rating.update_rating(rating=rating, feedback=feedback)
        except Exception as e:
            payload = {"order_id": order_id, "customer_id": customer_id}
            get_logger().error(ErrorCodes.UPDATE_ORDER_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.UPDATE_ORDER_RATING_ERROR, payload=payload) from e

    @staticmethod
    async def get_rating(order_id: str) -> Dict[str, Any]:
        try:
            order_rating = await OrderRating.fetch_document(order_id=order_id)
            if not order_rating:
                raise BaseError(error_code=ErrorCodes.ORDER_RATING_NOT_FOUND_ERROR, payload={"order_id": order_id})
            return order_rating.dict()
        except Exception as e:
            payload = {"order_id": order_id}
            get_logger().error(ErrorCodes.GET_ORDER_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.GET_ORDER_RATING_ERROR, payload=payload) from e
    
    @staticmethod
    async def get_customer_order_ratings(customer_id: str) -> List[Dict[str, Any]]:
        try:
            order_ratings = await OrderRatingModel.find_all(customer_id=customer_id)
            return [order_rating.dict() for order_rating in order_ratings]
        except Exception as e:
            payload = {"customer_id": customer_id}
            get_logger().error(ErrorCodes.GET_ORDER_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.GET_ORDER_RATING_ERROR, payload=payload) from e
        
    @staticmethod
    async def get_restaurant_order_ratings(restaurant_id: str) -> List[Dict[str, Any]]:
        try:
            order_ratings = await OrderRatingModel.find_all(restaurant_id=restaurant_id)
            return [order_rating.dict() for order_rating in order_ratings]
        except Exception as e:
            payload = {"restaurant_id": restaurant_id}
            get_logger().error(ErrorCodes.GET_ORDER_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.GET_ORDER_RATING_ERROR, payload=payload) from e
