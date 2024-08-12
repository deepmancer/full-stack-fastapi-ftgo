from typing import Dict, Any

from config import LayerNames, BaseConfig
from data_access.broker import RPCBroker
from ftgo_utils.enums import ResponseStatus
from ftgo_utils.errors import ErrorCodes
from ftgo_utils.logger import get_logger

logger = get_logger(layer=LayerNames.MESSAGE_BROKER.value, environment=BaseConfig.load_environment())

class Microservice:
    _service_name = ''

    @classmethod
    async def _call_rpc(cls, event_name: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        try:
            rpc_client = RPCBroker.get_client()
            response = await rpc_client.call(event_name, data=data, **kwargs)
            if response.get('status') not in [status.value for status in ResponseStatus]:
                raise ValueError(f"Invalid response status: {response}")
            return response
        except Exception as e:
            logger.error(f"Exception at calling event: {event_name} in service: {cls._service_name}: {e}")
            return {
                "response": ResponseStatus.ERROR.value,
                "error_code": ErrorCodes.UNKNOWN_ERROR.value,
            }
