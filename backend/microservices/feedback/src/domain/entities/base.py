from pydoc import doc
from beanie import Document
from config import RedisConfig
from ftgo_utils.errors import ErrorCodes
from typing import Any, Dict, Optional
from data_access.cache_repository import CacheRepository


class BaseEntity:
    document_cls = None

    def __init__(self, document: Document):
        self.document: Document = document

    @classmethod
    def create(cls, **kwargs) -> "BaseEntity":
        raise NotImplementedError("The 'create' method must be implemented in the subclass.")

    @classmethod
    def build_query(cls, **kwargs) -> Dict[str, Any]:
        query = {}
        for key, value in kwargs.items():
            if value is not None:
                query[key] = value
        return query

    @classmethod
    async def fetch_document(cls, **kwargs) -> Optional[Document]:
        query = cls.build_query(**kwargs)
        document = await cls.document_cls.find(**query).first_or_none()
        return document

    @classmethod
    async def load(cls, **kwargs) -> Optional["BaseEntity"]:
        raise NotImplementedError("The 'save' method must be implemented in the subclass.")

    async def save(self):
        raise NotImplementedError("The 'save' method must be implemented in the subclass.")

    async def delete(self):
        raise NotImplementedError("The 'delete' method must be implemented in the subclass.")

    async def update(self, **kwargs):
        raise NotImplementedError("The 'update' method must be implemented in the subclass.")
