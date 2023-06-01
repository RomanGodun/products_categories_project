from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.actions.business_funcs import (
    select_category_products_,
    select_product_categories_,
    select_product_category_pairs_,
)
from app.api.schemas.business_funcs import (
    CategoriesSchema,
    ProductsSchema,
    ProductsToCategoriesSchema,
)
from app.database.session_utils import get_session

business_funcs_router = APIRouter()


@business_funcs_router.get("/select_product_categories", response_model=list[ProductsSchema])
async def select_product_categories(session: AsyncSession = Depends(get_session)):
    return await select_product_categories_(session)


@business_funcs_router.get("/select_category_products", response_model=list[CategoriesSchema])
async def select_category_products(session: AsyncSession = Depends(get_session)):
    return await select_category_products_(session)


@business_funcs_router.get("/select_product_category_pairs", response_model=list[ProductsToCategoriesSchema])
async def select_product_category_pairs(session: AsyncSession = Depends(get_session)):
    return await select_product_category_pairs_(session)
