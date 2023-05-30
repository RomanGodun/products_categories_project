from typing import List

from app.api.schemas.business_funcs import CategoriesSchema, ProductsSchema, ProductsToCategoriesSchema
from app.config.config import logger
from app.database.dals.base_dal import READ_TYPE, BaseDAL
from app.database.models.buisiness_entities import Product, Category, ProductToCategory
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def select_product_categories_(session: AsyncSession) -> List[ProductsSchema]:
        sel = (
                select( 
                        Product.title.label("product"),
                        func.array_agg(
                        Category.title
                        ).label("categories")       
                )
                .join_from(Product, ProductToCategory)
                .join(Category)
                .group_by(Product.id)
                .order_by(Product.title)
        )
        
        products = await BaseDAL(session).read(sel, READ_TYPE.ALL)
        logger.debug(products)
        return [ProductsSchema(product=p.product, categories=p.categories) for p in products]



async def select_category_products_(session: AsyncSession) -> List[CategoriesSchema]: 
        sel = (
                select(
                        Category.title.label("category"),
                        func.array_agg(
                        Product.title
                        ).label("products")
                )
                .join_from(Category, ProductToCategory)
                .join(Product)
                .group_by(Category.id)
                .order_by(Category.title)
        )
        
        categories = await BaseDAL(session).read(sel, READ_TYPE.ALL)
        logger.debug(categories)
        return [CategoriesSchema(category=c.category, products=c.products) for c in categories]



async def select_product_category_pairs_(session: AsyncSession) -> List[ProductsToCategoriesSchema]:
        sel = (
                select(
                        Product.title.label("product"),
                        Category.title.label("category")
                )
                .join_from(Product, ProductToCategory)
                .join(Category)
                .order_by(Product.title)
        )
        
        product_categories = await BaseDAL(session).read(sel, READ_TYPE.ALL)
        logger.info(product_categories)
        return [ProductsToCategoriesSchema(product=pc.product, category=pc.category) for pc in product_categories]

