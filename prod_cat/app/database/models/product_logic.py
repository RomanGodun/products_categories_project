from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import SCHEMES, Base, TimestampMixin

# задаем схему для таблиц этого файла
SCHEMA = SCHEMES.PRODUCT_LOGIC.value



class Product(TimestampMixin, Base):
    __table_args__ = {"schema": SCHEMA}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), unique=True)
    categories: Mapped[List["ProductToCategory"]] = relationship(back_populates="product")


class Category(TimestampMixin, Base):
    __table_args__ = {"schema": SCHEMA}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True)
    products: Mapped[List["ProductToCategory"]] = relationship(back_populates="category")


class ProductToCategory(TimestampMixin, Base):
    __table_args__ = {"schema": SCHEMA}
    
    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), primary_key=True)
    
    category: Mapped["Category"] = relationship(back_populates="products")
    product: Mapped["Product"] = relationship(back_populates="categories")

    

