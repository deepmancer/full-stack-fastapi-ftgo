from typing import Dict

from ftgo_utils.logger import get_logger

from config import LayerNames, BaseConfig
from data_access.broker import RPCBroker


logger = get_logger(layer=LayerNames.MESSAGE_BUS.value, environment=BaseConfig.load_environment())

class Microservice:
    _service_name = ''
        
    @classmethod
    async def _call_rpc(cls, event_name: str, data: Dict, **kwargs) -> Dict:
        try:
            rpc_client = await RPCBroker.get_client()
            response = await rpc_client.call(event_name, data=data, **kwargs)
            return response
        except Exception as e:
            logger.error(f"Exception at event: {event_name} and service: {cls._service_name}: {e}")
            return {'error': 'internal error', 'service': cls._service_name, 'event': event_name}
