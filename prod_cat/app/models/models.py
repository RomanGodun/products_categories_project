from __future__ import annotations
from typing import Set, List
from app.models.base import Base, TimestampMixin
from sqlalchemy import Column, ForeignKey, Table, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProductToCategory(TimestampMixin, Base):
    
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), primary_key=True)
    
    category: Mapped["Category"] = relationship(back_populates="products")
    product: Mapped["Product"] = relationship(back_populates="categories")


class Product(TimestampMixin, Base):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), unique=True)
    categories: Mapped[List["ProductToCategory"]] = relationship(back_populates="product")


class Category(TimestampMixin, Base):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True)
    products: Mapped[List["ProductToCategory"]] = relationship(back_populates="category")




    

