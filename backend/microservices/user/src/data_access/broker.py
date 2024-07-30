import asyncio

from ftgo_utils.errors import ErrorCodes
from rabbitmq_rpc import RPCClient, RabbitMQConfig

from data_access import get_logger
from config.broker import BrokerConfig
from config import LayerNames
from utils import handle_exception


class RPCBroker:
    _instance: 'RPCBroker' = None

    def __init__(self, rpc_client: RPCClient):
        self._rpc_client = rpc_client

    @classmethod
    async def initialize(cls, loop: asyncio.AbstractEventLoop = None) -> None:
        logger = get_logger(layer=LayerNames.MESSAGE_BROKER.value)

        if cls._instance is not None:
            return

        broker_config = BrokerConfig()

        try:
            config = RabbitMQConfig(
                host=broker_config.host,
                port=broker_config.port,
                user=broker_config.user,
                password=broker_config.password,
                vhost=broker_config.vhost,
                ssl=False,
            )
            rpc_client = await RPCClient.create(config=config)

            if loop is not None:
                rpc_client.set_event_loop(loop)

            cls._instance = cls(rpc_client)
        except Exception as e:
            message = "Failed to create an RPC Client"
            logger.exception(message, payload=config.dict())
            await handle_exception(e=e, error_code=ErrorCodes.RABBITMQ_CONNECTION_ERROR, message=message, payload=config.dict())

    @classmethod
    def get_instance(cls) -> 'RPCBroker':
        if cls._instance is None:
            raise Exception("RPCBroker has not been initialized. Call 'initialize' first.")
        return cls._instance

    @classmethod
    def get_client(cls) -> RPCClient:
        if cls._instance is None:
            raise Exception("RPCBroker has not been initialized. Call 'initialize' first.")
        return cls._instance._rpc_client

    @classmethod
    async def terminate(cls) -> None:
        if cls._instance is not None:
            await cls._instance._rpc_client.close()
            cls._instance = None
