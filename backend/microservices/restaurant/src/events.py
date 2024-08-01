import asyncio

from ftgo_utils.logger import get_logger
from ftgo_utils.errors import ErrorCodes

from application import MenuService, RestaurantService
from application.middleware import event_middleware
from config import LayerNames
from data_access.broker import RPCBroker
from utils import handle_exception

async def register_events():
    rpc_broker = RPCBroker.get_instance()
    rpc_client = rpc_broker.get_client()
    events_handlers = {
        'restaurant.supplier.register': RestaurantService.register,
        'restaurant.supplier.get_restaurant_info': RestaurantService.get_restaurant_info,
        'restaurant.supplier.get_supplier_restaurant_info': RestaurantService.get_supplier_restaurant_info,
        'restaurant.supplier.update_information': RestaurantService.update_information,
        'restaurant.supplier.delete_restaurant': RestaurantService.delete_restaurant,
        'restaurant.supplier.get_all_restaurant_info': RestaurantService.get_all_restaurant_info,
        'restaurant.menu.add_item': MenuService.add_item,
        'restaurant.menu.update_item': MenuService.update_item,
        'restaurant.menu.delete_item': MenuService.delete_item,
        'restaurant.menu.get_item_info': MenuService.get_item_info,
        'restaurant.menu.get_all_menu_item': MenuService.get_all_menu_item,
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
