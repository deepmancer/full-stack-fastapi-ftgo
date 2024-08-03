from typing import Any


class BaseRepository:
    _data_access = None

    @classmethod
    async def initialize(cls) -> None:
        raise NotImplementedError

    @classmethod
    async def terminate(cls) -> None:
        if cls._data_access:
            await cls._data_access.disconnect()
            cls._data_access = None
