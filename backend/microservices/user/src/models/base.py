import typing
from typing import Container, Optional, Type

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, ColumnProperty
from sqlalchemy.inspection import inspect
from pydantic import BaseModel, create_model, BaseConfig

class OrmConfig(BaseConfig):
    orm_mode = True

class DBTable(DeclarativeBase):
    metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()

    @classmethod
    def to_pydantic(
        cls, *, config: Type[BaseConfig] = OrmConfig, exclude: Container[str] = []
    ) -> Type[BaseModel]:
        mapper = inspect(cls)
        fields = {}
        for attr in mapper.attrs:
            if isinstance(attr, ColumnProperty):
                if attr.columns:
                    name = attr.key
                    if name in exclude:
                        continue
                    column = attr.columns[0]
                    python_type: Optional[type] = None
                    if hasattr(column.type, "impl"):
                        if hasattr(column.type.impl, "python_type"):
                            python_type = column.type.impl.python_type
                    elif hasattr(column.type, "python_type"):
                        python_type = column.type.python_type
                    assert python_type, f"Could not infer python_type for {column}"
                    default = None
                    if column.default is None and not column.nullable:
                        default = ...
                    fields[name] = (python_type, default)
        pydantic_model = create_model(
            cls.__name__, __config__=config, **fields
        )
        return pydantic_model

Base: typing.Type[DeclarativeBase] = DBTable
