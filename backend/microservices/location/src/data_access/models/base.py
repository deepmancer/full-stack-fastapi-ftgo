from datetime import datetime
from typing import Dict, Type, Any

import sqlalchemy
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ftgo_utils.uuid_gen import uuid4

from dto import BaseDTO

class Base(DeclarativeBase):
    __abstract__ = True
    metadata = sqlalchemy.MetaData()

    id: Mapped[str] = mapped_column(
        sqlalchemy.String, primary_key=True, default=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.to_dict()})>"

    @classmethod
    def from_dto(cls, dto: BaseDTO) -> 'Base':
        raise NotImplementedError

    def to_dto(self) -> BaseDTO:
        raise NotImplementedError
