from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from base import Base


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_name = Column(String(100))

    def __repr__(self):
        return f"Products(id={self.id!r}, product_name={self.product_name!r})"


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    category_name = Column(String(100))

    def __repr__(self):
        return f"Categories(id={self.id!r}, category_name={self.category_name!r})"


class ProductsCategories(Base):
    __tablename__ = "products_categories"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    def __repr__(self):
        return f"Categories(id={self.id!r}, product_id={self.product_id!r},category_id={self.category_id!r})"
