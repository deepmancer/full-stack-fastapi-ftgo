from typing import Dict, Any, Optional, List
from ftgo_utils.enums import DeliveryStatus
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger
from models import DeliveryRating as DeliveryRatingModel
from models import OrderRating as OrderRatingModel
from utils import handle_exception
from domain.entities.delivery_rating import DeliveryRating
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger

class DeliveryRatingHandler:
    @staticmethod
    async def create_delivery_rating(delivery_id: str, order_id: str, customer_id: str, rating: int, feedback: Optional[str] = None, driver_id: Optional[str] = None) -> DeliveryRating:
        try:
            delivery_rating = DeliveryRating.create(delivery_id=delivery_id, order_id=order_id, customer_id=customer_id, rating=rating, feedback=feedback, driver_id=driver_id)
            await delivery_rating.save()
            return delivery_rating
        except Exception as e:
            payload = {"delivery_id": delivery_id, "order_id": order_id, "customer_id": customer_id}
            get_logger().error(ErrorCodes.CREATE_DELIVERY_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.CREATE_DELIVERY_RATING_ERROR, payload=payload) from e

    @staticmethod
    async def update_delivery_rating(delivery_id: str, order_id: str, customer_id: str, rating: int, feedback: Optional[str] = None):
        try:
            delivery_rating = await DeliveryRating.load(delivery_id=delivery_id, order_id=order_id, customer_id=customer_id)
            if not delivery_rating:
                raise BaseError(error_code=ErrorCodes.DELIVERY_RATING_NOT_FOUND_ERROR, payload={"delivery_id": delivery_id, "order_id": order_id})
            await delivery_rating.update_rating(rating=rating, feedback=feedback)
        except Exception as e:
            payload = {"delivery_id": delivery_id, "order_id": order_id, "customer_id": customer_id}
            get_logger().error(ErrorCodes.UPDATE_DELIVERY_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.UPDATE_DELIVERY_RATING_ERROR, payload=payload) from e

    @staticmethod
    async def get_rating(order_id: str) -> Dict[str, Any]:
        try:
            delivery_rating = await DeliveryRating.fetch_document(order_id=order_id)
            if not delivery_rating:
                raise BaseError(error_code=ErrorCodes.DELIVERY_RATING_NOT_FOUND_ERROR, payload={"order_id": order_id})
            return delivery_rating.dict()
        except Exception as e:
            payload = {"order_id": order_id}
            get_logger().error(ErrorCodes.GET_DELIVERY_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.GET_DELIVERY_RATING_ERROR, payload=payload) from e
        
    @staticmethod
    async def get_customer_delivery_ratings(customer_id: str) -> List[Dict[str, Any]]:
        try:
            delivery_ratings = await DeliveryRatingModel.find_all(customer_id=customer_id)
            return [delivery_rating.dict() for delivery_rating in delivery_ratings]
        except Exception as e:
            payload = {"customer_id": customer_id}
            get_logger().error(ErrorCodes.GET_DELIVERY_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.GET_DELIVERY_RATING_ERROR, payload=payload) from e
        
    @staticmethod
    async def get_driver_delivery_ratings(driver_id: str) -> List[Dict[str, Any]]:
        try:
            delivery_ratings = await DeliveryRatingModel.find_all(driver_id=driver_id)
            return [delivery_rating.dict() for delivery_rating in delivery_ratings]
        except Exception as e:
            payload = {"driver_id": driver_id}
            get_logger().error(ErrorCodes.GET_DELIVERY_RATING_ERROR.value, payload=payload)
            raise BaseError(error_code=ErrorCodes.GET_DELIVERY_RATING_ERROR, payload=payload) from e
