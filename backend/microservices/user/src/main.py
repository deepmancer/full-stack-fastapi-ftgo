import asyncio
import uvloop
from ftgo_utils.logger import init_logging

from config import ServiceConfig
from data_access.events.lifecycle import setup, teardown
from events import EventManager

async def main():
    service_config = ServiceConfig.load()
    init_logging(level=service_config.log_level)

    await setup()
    event_manager = await EventManager.create(loop=asyncio.get_event_loop())
    await event_manager.define_events()

    await asyncio.Future()

if __name__ == '__main__':
    uvloop.install()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(teardown())
        loop.close()
