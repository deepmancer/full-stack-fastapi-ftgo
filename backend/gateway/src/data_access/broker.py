import asyncio
from ftgo_utils.logger import get_logger
from rabbitmq_rpc import RPCClient, RabbitMQConfig

from config import BaseConfig, LayerNames, env_var

class EventManager:
    _instance = None
    _lock = asyncio.Lock()

    def __init__(self, rpc_client: RPCClient):
        self._rpc_client = rpc_client

    @classmethod
    async def create(cls, loop: asyncio.AbstractEventLoop = None) -> 'EventManager':
        async with cls._lock:
            if cls._instance is None:
                if loop is None:
                    loop = asyncio.get_event_loop()
                cls._instance = await cls._create_instance(loop)
        return cls._instance

    @classmethod
    async def _create_instance(cls, loop: asyncio.AbstractEventLoop) -> 'EventManager':
        BaseConfig.load()
        logger = get_logger(layer_name=LayerNames.MESSAGE_BUS.value, environment=BaseConfig.load_environment())
        try:
            rpc_client = await RPCClient.create(
                host=env_var("RABBITMQ_HOST"),
                port=env_var("RABBITMQ_PORT", cast_type=int),
                user=env_var("RABBITMQ_USER"),
                password=env_var("RABBITMQ_PASS"),
                vhost=env_var("RABBITMQ_VHOST", default="/"),
                ssl=env_var("RABBITMQ_SSL_CONNECTION", default=False, cast_type=lambda s: s.lower() in ['true', '1']),
                logger=logger,
            )
            rpc_client.set_event_loop(loop)

            return EventManager(rpc_client)
        except Exception as e:
            logger.error(f"Failed to create EventManager: {e}")
            raise

    @classmethod
    async def rpc_client(cls, loop: asyncio.AbstractEventLoop = None) -> RPCClient:
        instance = await cls.create(loop)
        return instance._rpc_client
