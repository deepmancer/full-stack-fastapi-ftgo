import asyncio
import uvloop
from dotenv import load_dotenv

from ftgo_utils.logger import init_logging

from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown
from data_access.broker import RPCBroker
from events import register_events

load_dotenv()

async def startup_event():
    await setup()
    await RPCBroker.initialize(loop=asyncio.get_event_loop())
    
    rpc_broker = RPCBroker.get_instance()
    await register_events(rpc_broker=rpc_broker)

    await asyncio.Future()

async def shutdown_event():
    await teardown()
    await RPCBroker.close()

if __name__ == '__main__':
    uvloop.install()
    loop = asyncio.get_event_loop()

    service_config = ServiceConfig()
    init_logging(level=service_config.log_level)

    try:
        loop.run_until_complete(startup_event())
    finally:
        loop.run_until_complete(shutdown_event())
        loop.close()
