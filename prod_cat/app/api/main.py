from contextlib import asynccontextmanager

import app.database.queries.product_logic as product_query
from app.api.schemas import (CategoriesSchema, ProductsSchema,
                             ProductsToCategoriesSchema)
from app.config.config import logger
from app.database.queries.qutils import READ_TYPE, read
from app.database.session_utils import connect, disconnect, get_session
from fastapi import FastAPI, Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect()
    yield
    disconnect()

 
app = FastAPI(lifespan=lifespan)


    
@app.get("/products", response_model=list[ProductsSchema])
async def get_products(session: AsyncSession = Depends(get_session)):
    products = await read(product_query.select_product_categories, session, READ_TYPE.ALL)
    logger.debug(products)
    return [ProductsSchema(product=p.product, categories=p.categories) for p in products]


@app.get("/categories", response_model=list[CategoriesSchema])
async def get_categories(session: AsyncSession = Depends(get_session)):
    categories = await read(product_query.select_category_products, session, READ_TYPE.ALL)
    logger.debug(categories)
    return [CategoriesSchema(category=c.category, products=c.products) for c in categories]


@app.get("/product_categories", response_model=list[ProductsToCategoriesSchema])
async def get_products_categories(session: AsyncSession = Depends(get_session)):
    product_categories = await read(product_query.select_product_category_pairs, session, READ_TYPE.ALL)
    logger.debug(product_categories)
    return [ProductsToCategoriesSchema(product=pc.product, category=pc.category) for pc in product_categories]

