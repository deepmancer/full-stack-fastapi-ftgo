import asyncio

from ftgo_utils.logger import get_logger
from ftgo_utils.errors import ErrorCodes

from application import VehicleService, AddressService, ProfileService
from application.middleware import event_middleware
from config import LayerNames
from data_access.broker import RPCBroker
from utils import handle_exception

async def register_events():
    rpc_broker = RPCBroker.get_instance()
    rpc_client = rpc_broker.get_client()
    events_handlers = {
        'user.profile.create': ProfileService.register,
        'user.address.add_address': AddressService.add_address,
        'user.profile.verify_account': ProfileService.verify_account,
        'user.profile.resend_auth_code': ProfileService.resend_auth_code,
        'user.profile.login': ProfileService.login,
        'user.profile.get_info': ProfileService.get_info,
        'user.profile.delete_account': ProfileService.delete_account,
        'user.profile.logout': ProfileService.logout,
        'user.profile.update_profile': ProfileService.update_profile,
        'user.address.get_default_address': AddressService.get_default_address,
        'user.address.delete': AddressService.delete_address,
        'user.address.set_preferred_address': AddressService.set_preferred_address,
        'user.address.get_address_info': AddressService.get_address_info,
        'user.address.get_all_addresses': AddressService.get_all_addresses,
        'user.address.update_information': AddressService.update_information,
        'driver.vehicle.get_info': VehicleService.get_vehicle_info,
        'driver.vehicle.register': VehicleService.register_vehicle,
        'driver.vehicle.delete': VehicleService.delete_vehicle,
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
