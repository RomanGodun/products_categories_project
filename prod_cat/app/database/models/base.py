import re
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

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


