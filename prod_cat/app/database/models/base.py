import re
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)
from sqlalchemy.sql import func
from pydantic import BaseModel

class Schemes(str, Enum):
    PUBLIC = "public"
    BUISINESS_ENTITIES = "buisiness_entities"


class Base(AsyncAttrs, DeclarativeBase):

    __table_args__ = {
        "schema": Schemes.PUBLIC.value,
        "extend_existing": True,
    }

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(
            r"(?<!^)(?=[A-Z])", "_", cls.__name__
        ).lower()  # translate from CamelCase to snake_case
        
        
    def as_dict(self, drop_base_fields: bool = True, wo_none: bool = False) -> dict:
        if drop_base_fields:
            drop_fields = ["id", "created_at", "edited_at"]
        else:
            drop_fields = []

        fields = inspect(self).mapper.column_attrs
        attributes = {c.key: getattr(self, c.key) for c in fields if c.key not in drop_fields}
        
        if wo_none:
            attributes = {k: v for k, v in attributes.items() if v is not None}
            
        return attributes
    
    @classmethod
    def from_dto(cls, dto:BaseModel):
        obj = cls()
        properties = dict(dto)
        for key, value in properties.items():
            try:       
                if cls.is_pydantic(value):
                    value = getattr(cls, key).property.mapper.class_.from_dto(value)
                setattr(obj, key, value)
            except AttributeError as e:
                raise AttributeError(e)
        return obj
    
    @staticmethod
    def is_pydantic(obj: object):
        """Checks whether an object is pydantic."""
        return type(obj).__class__.__name__ == "ModelMetaclass"
    
    
    def __repr__(self):
        fields = self.__dict__.copy()
        fields.pop("_sa_instance_state")
        return str(self.__class__.__name__) + ": " + str(fields)

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    edited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


