from sqlalchemy import join, select, func, literal_column
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Product, Category, ProductToCategory
from app.config.config import logger
from sqlalchemy.ext.asyncio import async_sessionmaker


# async def run_some_sql(async_session: async_sessionmaker[AsyncSession]) -> None:
#     async with async_session() as session:
#         session.add(SomeObject(data="object"))
#         session.add(SomeOtherObject(name="other object"))
#         await session.commit()

# async def main() -> None:
    

#     await run_some_sql(async_session)

#     await engine.dispose()


async def get_products(async_session: async_sessionmaker[AsyncSession]) -> list:
    sel = (
        select(
                Product.product_name.label("product"),
                func.array_agg(
                    Category.category_name #, literal_column("' , '")
                ).label("categories")
        )
        .join_from(Product, ProductToCategory)
        .join(Category)
        .group_by(Product.product_name)
        .order_by(Product.product_name)
    )
    
    async with async_session() as session:
        result = await session.execute(sel)
        
    return result.all()


# def get_categories(session: AsyncSession) -> list:
#     sel = (
#         select(
#             [
#                 Category.category_name.label("category"),
#                 func.string_agg(Product.product_name, literal_column("','")).label(
#                     "products"
#                 ),
#             ]
#         )
#         .select_from(
#             join(
#                 Category,
#                 ProductToCategory,
#                 Category.id == ProductToCategory.category_id,
#                 isouter=True,
#             ).join(
#                 Product,
#                 Product.id == ProductToCategory.product_id,
#                 isouter=True,
#             )
#         )
#         .group_by(
#             Category.category_name,
#         )
#         .order_by(
#             Category.category_name,
#         )
#     )
#     result = session.execute(sel)
#     return result.all()


# def get_products_categories(session: AsyncSession) -> list:

#     sel = (
#         select(
#             [
#                 Product.product_name.label("product"),
#                 Category.category_name.label("category"),
#             ]
#         )
#         .select_from(
#             join(
#                 Product,
#                 ProductToCategory,
#                 Product.id == ProductToCategory.product_id,
#                 isouter=False,
#             ).join(
#                 Category,
#                 Category.id == ProductToCategory.category_id,
#                 isouter=False,
#             )
#         )
#         .order_by(
#             Product.product_name,
#         )
#     )
#     result = session.execute(sel)
#     return result.all()
