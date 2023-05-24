import re
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)
from sqlalchemy.sql import func


class SCHEMES(str, Enum):
    PUBLIC = "public"
    PRODUCT_LOGIC = "public"


class Base(AsyncAttrs, DeclarativeBase):

    __table_args__ = {
        "schema": SCHEMES.PUBLIC.value,
        "extend_existing": True,
    }

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(
            r"(?<!^)(?=[A-Z])", "_", cls.__name__
        ).lower()  # translate from CamelCase to snake_case

    id: Mapped[int] = mapped_column(primary_key=True, index=True)


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


