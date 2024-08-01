import asyncio

from ftgo_utils.logger import get_logger
from ftgo_utils.errors import ErrorCodes

from application import DriverService, TrackerService
from application.middleware import event_middleware
from config import LayerNames
from data_access.broker import RPCBroker
from utils import handle_exception

async def register_events():
    rpc_broker = RPCBroker.get_instance()
    rpc_client = rpc_broker.get_client()
    events_handlers = {
        'driver.location.submit': DriverService.submit_location,
        'driver.status.online': DriverService.change_status_online,
        'driver.status.offline': DriverService.change_status_offline,
        'driver.availability.available': DriverService.set_driver_available,
        'driver.availability.occupied': DriverService.set_driver_occupied,
        'driver.location.get': DriverService.get_last_location,
        'driver.status.get': DriverService.get_driver_status,
        'location.drivers.get_nearest': TrackerService.get_nearest_drivers,
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
