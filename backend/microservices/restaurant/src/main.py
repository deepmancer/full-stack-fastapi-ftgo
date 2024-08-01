import asyncio
import uvloop
from dotenv import load_dotenv

from ftgo_utils.logger import init_logging

from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown
from events import register_events

load_dotenv()

async def setup_env():
    service_config = ServiceConfig()
    init_logging(level=service_config.log_level)

async def startup_event():
    await setup_env()
    await setup()
    await asyncio.sleep(1)
    await register_events()
    await asyncio.Future()

async def shutdown_event():
    await teardown()

if __name__ == '__main__':
    uvloop.install()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(startup_event())
    finally:
        loop.run_until_complete(shutdown_event())
        loop.close()
