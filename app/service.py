from sqlalchemy import join, select, func, literal_column
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import *


async def get_products(session: AsyncSession) -> list:
    sel = (
        select(
            [
                Products.product_name.label("product"),
                func.string_agg(
                    Categories.category_name, literal_column("' , '")
                ).label("categories"),
            ]
        )
        .select_from(
            join(
                Products,
                ProductsCategories,
                Products.id == ProductsCategories.product_id,
                isouter=True,
            ).join(
                Categories,
                Categories.id == ProductsCategories.category_id,
                isouter=True,
            )
        )
        .group_by(
            Products.product_name,
        )
        .order_by(
            Products.product_name,
        )
    )
    result = await session.execute(sel)
    return result.all()


async def get_categories(session: AsyncSession) -> list:
    sel = (
        select(
            [
                Categories.category_name.label("category"),
                func.string_agg(Products.product_name, literal_column("','")).label(
                    "products"
                ),
            ]
        )
        .select_from(
            join(
                Categories,
                ProductsCategories,
                Categories.id == ProductsCategories.category_id,
                isouter=True,
            ).join(
                Products,
                Products.id == ProductsCategories.product_id,
                isouter=True,
            )
        )
        .group_by(
            Categories.category_name,
        )
        .order_by(
            Categories.category_name,
        )
    )
    result = await session.execute(sel)
    return result.all()


async def get_products_categories(session: AsyncSession) -> list:

    sel = (
        select(
            [
                Products.product_name.label("product"),
                Categories.category_name.label("category"),
            ]
        )
        .select_from(
            join(
                Products,
                ProductsCategories,
                Products.id == ProductsCategories.product_id,
                isouter=False,
            ).join(
                Categories,
                Categories.id == ProductsCategories.category_id,
                isouter=False,
            )
        )
        .order_by(
            Products.product_name,
        )
    )
    result = await session.execute(sel)
    return result.all()
