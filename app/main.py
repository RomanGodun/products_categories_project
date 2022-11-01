from pydantic import BaseModel

from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from base import get_session
import service
from initlog import getСustomLogger
import os


logger = getСustomLogger(
    servicename="product_service",
    filepath="/var/log/product_service/product_service.log",
    levelG=int(os.environ["LOG_G"]),
)

app = FastAPI()


class ProductsSchema(BaseModel):
    product: str
    categories: str | None


class CategoriesSchema(BaseModel):
    category: str
    products: str | None


class ProductsCategoriesSchema(BaseModel):
    product: str
    category: str


@app.get("/products", response_model=list[ProductsSchema])
async def get_products(session: AsyncSession = Depends(get_session)):
    try:
        products = await service.get_products(session)
        logger.debug(f"{products}")
        result = [
            ProductsSchema(product=p.product, categories=p.categories) for p in products
        ]
        logger.info("products with categories have been successfully received")
    except:
        logger.exception(f"/products was failed")
    return result


@app.get("/categories", response_model=list[CategoriesSchema])
async def get_categories(session: AsyncSession = Depends(get_session)):
    try:
        categories = await service.get_categories(session)
        logger.debug(f"{categories}")
        result = [
            CategoriesSchema(category=c.category, products=c.products)
            for c in categories
        ]
        logger.info("categories with products have been successfully received")
    except:
        logger.exception(f"/categories was failed")

    return result


@app.get("/product_categories", response_model=list[ProductsCategoriesSchema])
async def get_products_categories(session: AsyncSession = Depends(get_session)):
    try:
        product_categories = await service.get_products_categories(session)
        logger.debug(f"{product_categories}")
        result = [
            ProductsCategoriesSchema(product=pc.product, category=pc.category)
            for pc in product_categories
        ]
        logger.info("list of product-category have been successfully received")
    except:
        logger.exception(f"/product_categories was failed")

    return result
