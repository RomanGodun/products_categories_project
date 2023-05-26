# from app.database.session_utils import get_session
# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# basic_router = APIRouter()

# @basic_router.get("/select_product_categories", response_model=list[ProductsSchema])
# async def select_product_categories(session: AsyncSession = Depends(get_session)):
#     return await 

# @basic_router.get("/select_category_products", response_model=list[CategoriesSchema])
# async def select_category_products(session: AsyncSession = Depends(get_session)):
#     return await 

# @basic_router.get("/select_product_category_pairs", response_model=list[ProductsToCategoriesSchema])
# async def select_product_category_pairs(session: AsyncSession = Depends(get_session)):
#     return await 