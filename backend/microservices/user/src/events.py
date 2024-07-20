import asyncio
from ftgo_utils.logger import get_logger
from rabbitmq_rpc import RPCClient, RabbitMQConfig

from application import VehicleService, AddressService, ProfileService
from config import BaseConfig, LayerNames, env_var


class EventManager:
    def __init__(self, rpc_client: RPCClient):
        """
        Initializes the EventManager with an RPC client.
        
        :param rpc_client: An instance of RPCClient.
        """
        self.rpc_client = rpc_client

    @staticmethod
    async def create(loop: asyncio.AbstractEventLoop):
        """
        Static method to create an instance of EventManager.
        
        :param loop: An instance of asyncio.AbstractEventLoop.
        :return: An instance of EventManager.
        """
        BaseConfig.load()
        logger = get_logger(layer_name=LayerNames.MESSAGE_BUS.value, environment=BaseConfig.load_environment())
        try:
            print(dict(
                host=env_var("RABBITMQ_HOST"),
                port=env_var("RABBITMQ_PORT", cast_type=int),
                user=env_var("RABBITMQ_USER"),
                password=env_var("RABBITMQ_PASS"),
                vhost=env_var("RABBITMQ_VHOST"),
                ssl=env_var("RABBITMQ_SSL_CONNECTION", default=False, cast_type=lambda x: True if x.lower() == "true" else False),
            ))
            rpc_client = await RPCClient.create(
                host=env_var("RABBITMQ_HOST"),
                port=env_var("RABBITMQ_PORT", cast_type=int),
                user=env_var("RABBITMQ_USER"),
                password=env_var("RABBITMQ_PASS"),
                vhost='/',
                ssl=env_var("RABBITMQ_SSL_CONNECTION", default=False, cast_type=lambda x: True if x.lower() == "true" else False),
                logger=logger,
            )
            # rpc_client.set_event_loop(loop)

            return EventManager(rpc_client)
        except Exception as e:
            logger.error(f"Failed to create EventManager: {e}")
            raise

    async def define_events(self):
        """
        Registers a series of events with corresponding handlers.
        """
        events_handlers = {
            'user.profile.create': ProfileService.register,
            'user.address.add_address': AddressService.add_address,
            'user.driver.vehicle.register_vehicle': VehicleService.register_vehicle,
            'user.profile.verify_account': ProfileService.verify_account,
            'user.profile.login': ProfileService.login,
            'user.profile.get_info': ProfileService.get_info,
            'user.profile.delete_account': ProfileService.delete_account,
            'user.profile.logout': ProfileService.logout,
            'user.profile.update_profile': ProfileService.update_profile,
            'user.profile.get_user_info_with_credentials': ProfileService.get_user_info_with_credentials,
            'user.address.get_default_address': AddressService.get_default_address,
            'user.address.delete_address': AddressService.delete_address,
            'user.address.set_preferred_address': AddressService.set_preferred_address,
            'user.address.get_address_info': AddressService.get_address_info,
            'user.address.get_all_addresses': AddressService.get_all_addresses,
            'user.address.update_address': AddressService.update_address,
            'user.driver.vehicle.get_info': VehicleService.get_vehicle_info,
        }

        for event, handler in events_handlers.items():
            try:
                await self.rpc_client.register_event(event=event, handler=handler)
                self.rpc_client.logger.info(f"Registered event '{event}' with handler '{handler.__name__}'")
            except Exception as e:
                self.rpc_client.logger.error(f"Failed to register event '{event}': {e}")
