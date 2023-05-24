import app.service as service
from app.config.config import logger
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from app.config.config import db_url
# from app.models.base import async_session

app = FastAPI()


class ProductsSchema(BaseModel):
    product: str
    categories: list | None


class CategoriesSchema(BaseModel):
    category: str
    products: str | None


class ProductsToCategoriesSchema(BaseModel):
    product: str
    category: str


@app.get("/products", response_model=list[ProductsSchema])
async def get_products():
    
    engine = create_async_engine(db_url, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    products = await service.get_products(async_session)
    
    logger.debug(f"{products}")
    
    result = [
        ProductsSchema(product=p.product, categories=p.categories) for p in products
    ]
    
    logger.info("products with categories have been successfully received")
    
    return result


# @app.get("/categories", response_model=list[CategoriesSchema])
# def get_categories(session: AsyncSession = Depends(get_session)):
#     try:
#         categories = service.get_categories(session)
#         logger.debug(f"{categories}")
#         result = [
#             CategoriesSchema(category=c.category, products=c.products)
#             for c in categories
#         ]
#         logger.info("categories with products have been successfully received")
#     except:
#         logger.exception(f"/categories was failed")

#     return result


# @app.get("/product_categories", response_model=list[ProductsToCategoriesSchema])
# def get_products_categories(session: AsyncSession = Depends(get_session)):
#     try:
#         product_categories = service.get_products_categories(session)
#         logger.debug(f"{product_categories}")
#         result = [
#             ProductsToCategoriesSchema(product=pc.product, category=pc.category)
#             for pc in product_categories
#         ]
#         logger.info("list of product-category have been successfully received")
#     except:
#         logger.exception(f"/product_categories was failed")

#     return result
