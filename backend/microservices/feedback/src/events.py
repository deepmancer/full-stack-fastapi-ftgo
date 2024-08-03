import asyncio

from ftgo_utils.logger import get_logger
from ftgo_utils.errors import ErrorCodes

from application.delivery import DeliveryRatingService
from application.order import OrderRatingService

from application.middleware import event_middleware
from config import LayerNames
from data_access.broker import RPCBroker
from utils import handle_exception

async def register_events():
    rpc_broker = RPCBroker.get_instance()
    rpc_client = rpc_broker.get_client()

    events_handlers = {
        # Delivery Rating Events
        'delivery.rating.create': DeliveryRatingService.create_delivery_rating,
        'delivery.rating.update': DeliveryRatingService.update_delivery_rating,
        'delivery.rating.get_details': DeliveryRatingService.get_delivery_rating,
        'delivery.rating.get_customer_ratings': DeliveryRatingService.get_customer_delivery_ratings,
        'delivery.rating.get_driver_ratings': DeliveryRatingService.get_driver_delivery_ratings,

        # Order Rating Events
        'order.rating.create': OrderRatingService.create_order_rating,
        'order.rating.update': OrderRatingService.update_order_rating,
        'order.rating.get_details': OrderRatingService.get_order_rating,
        'order.rating.get_customer_ratings': OrderRatingService.get_customer_order_ratings,
        'order.rating.get_restaurant_ratings': OrderRatingService.get_restaurant_order_ratings,
    }

    for event, _handler in events_handlers.items():
        try:
            handler = event_middleware(event, _handler)
            await rpc_client.register_event(event=event, handler=handler)
            rpc_client.logger.info(f"Registered event '{event}' with handler '{handler.__name__}'")
        except Exception as e:
            payload = {"event_name": event}
            rpc_client.logger.exception(ErrorCodes.EVENT_REGISTERATION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.EVENT_REGISTERATION_ERROR, payload=payload)
