import re
from datetime import datetime
from typing import Dict

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)
from sqlalchemy.sql import func


class Base(AsyncAttrs,DeclarativeBase):
    """define a series of common elements that may be applied to mapped
    classes using this class as a base class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()  # translate from CamelCase to snake_case

    __table_args__ = {"extend_existing": True}
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    edited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


Base.metadata.schema = "public"

