from typing import Any


class BaseRepository:
    _data_access = None

    @classmethod
    async def insert(cls, *args, **kwargs) -> Any:
        raise NotImplementedError

    @classmethod
    async def delete(cls, *args, **kwargs) -> Any:
        raise NotImplementedError

    @classmethod
    async def update(cls, *args, **kwargs) -> Any:
        raise NotImplementedError

    @classmethod
    async def fetch(cls, *args, **kwargs) -> Any:
        raise NotImplementedError

    @classmethod
    async def initialize(cls) -> None:
        raise NotImplementedError

    @classmethod
    async def terminate(cls) -> None:
        raise NotImplementedError
