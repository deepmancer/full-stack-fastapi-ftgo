import asyncio

from ftgo_utils.logger import get_logger
from rabbitmq_rpc import RPCClient

from config import BaseConfig, LayerNames, env_var

class RPCBroker:
    _instance: 'RPCBroker' = None

    def __init__(self, rpc_client: RPCClient):
        self._rpc_client = rpc_client

    @classmethod
    async def initialize(cls, loop: asyncio.AbstractEventLoop = None) -> None:
        if cls._instance is not None:
            return

        BaseConfig.load()
        logger = get_logger(
            layer_name=LayerNames.MESSAGE_BUS.value,
            environment=BaseConfig.load_environment()
        )

        try:
            rpc_client = await RPCClient.create(
                host=env_var("RABBITMQ_HOST"),
                port=env_var("RABBITMQ_PORT", default=5672, cast_type=int),
                user=env_var("RABBITMQ_USER"),
                password=env_var("RABBITMQ_PASS"),
                vhost=env_var("RABBITMQ_VHOST", default="/"),
                ssl=env_var("RABBITMQ_SSL_CONNECTION", default=False, cast_type=lambda s: s.lower() in ['true', '1']),
                logger=logger,
            )
            if loop is not None:
                rpc_client.set_event_loop(loop)

            cls._instance = cls(rpc_client)
        except Exception as e:
            logger.error(f"Failed to create an RPC Client: {e}")
            raise

    @classmethod
    def get_instance(cls) -> 'RPCBroker':
        if cls._instance is None:
            raise Exception("RPCBroker has not been initialized. Call 'initialize' first.")
        return cls._instance

    @classmethod
    def get_client(cls) -> RPCClient:
        return cls._rpc_client
