import asyncio

from ftgo_utils.logger import get_logger
from ftgo_utils.errors import ErrorCodes

from application.delivery import DeliveryService
from application.restaurant import RestaurantService
from application.order_status import OrderStatusService
from application.order import OrderService

from application.middleware import event_middleware
from config import LayerNames
from data_access.broker import RPCBroker
from utils import handle_exception

async def register_events():
    rpc_broker = RPCBroker.get_instance()
    rpc_client = rpc_broker.get_client()

    events_handlers = {
        # Order Lifecycle Events
        # 'order.history': OrderService.get_history,
        'order.create': OrderService.create_order,
        'order.update': OrderService.update_order,
        'order.cancel': OrderStatusService.cancel_order,
        'order.get_details': OrderService.get_order_details,

        # Order Status Events
        'order.status.change': OrderStatusService.change_order_status,

        # Delivery Coordination Events
        'order.delivery.update_status': DeliveryService.update_delivery_status,
        'order.delivery.get_details': DeliveryService.get_delivery_details,

        # Restaurant Events
        'order.restaurant.confirm': RestaurantService.confirm_order,
        'order.restaurant.reject': RestaurantService.reject_order,
        
        'order.delivery.driver_found': DeliveryService.assign_driver_to_delivery,
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

