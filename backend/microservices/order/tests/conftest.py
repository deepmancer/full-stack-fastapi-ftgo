import pytest
import asyncio
import pytest_asyncio

from test_doubles.time import TimeProvider

MOCKED_TIMESTAMP = 1704067200 # 2024, January 1	

@pytest.fixture(scope='function')
def time_machine():
    provider = TimeProvider(timestamp=MOCKED_TIMESTAMP)
    provider.start()
    yield provider
    provider.stop()

