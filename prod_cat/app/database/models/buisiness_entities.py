from __future__ import annotations

from typing import List
import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import Schemes, Base, TimestampMixin
from sqlalchemy.dialects.postgresql import ENUM

# задаем схему для таблиц этого файла
SCHEMA = Schemes.BUISINESS_ENTITIES.value

#ENUM for column rars
RARS = set(["0+", "6+", "12+", "16+", "18+"])
rars_t = ENUM(*RARS, schema=SCHEMA, name="rars_t")
       
    
class Product(TimestampMixin, Base):
    __table_args__ = {"schema": SCHEMA}
    
    title: Mapped[str] = mapped_column(String(100),nullable=False, comment='Title of the product', index=True)
    flammable: Mapped[bool] = mapped_column(nullable=False, comment='flammable product or not')
    price: Mapped[int] = mapped_column(nullable=False, comment='price displayed on the platform', index=True)
   
    categories: Mapped[List["Category"]] = relationship(secondary=f"{SCHEMA}.product_to_category", back_populates=f"products")


class Category(TimestampMixin, Base):
    __table_args__ = {"schema": SCHEMA}
    
    title: Mapped[str] = mapped_column(String(100),nullable=False, comment='Title of the category', index=True)
    rars: Mapped[ENUM] = mapped_column(rars_t, comment='Title of the category')
    
    products: Mapped[List[Product]] = relationship(secondary=f"{SCHEMA}.product_to_category", back_populates=f"categories")


class ProductToCategory(TimestampMixin, Base):
    __table_args__ = {"schema": SCHEMA}
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    product_id: Mapped[UUID] = mapped_column(ForeignKey(Product.id), primary_key=True)
    category_id: Mapped[UUID] = mapped_column(ForeignKey(Category.id), primary_key=True)
    

    


