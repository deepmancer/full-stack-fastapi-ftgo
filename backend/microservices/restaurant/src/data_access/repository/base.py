class BaseRepository:
    data_access = None

    @classmethod
    async def initialize(cls, configuration):
        raise NotImplementedError

    @classmethod
    async def terminate(cls):
        if cls._data_access is not None:
            await cls._data_access.disconnect()
