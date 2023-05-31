from contextlib import asynccontextmanager

from app.api.handlers.business_funcs import business_funcs_router
from app.api.handlers.moderation.category import category_router
from app.api.handlers.moderation.product import product_router
from app.database.session_utils import connect, disconnect
from fastapi import APIRouter, FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect()
    yield
    disconnect()


app = FastAPI(lifespan=lifespan)

# create the instance for the routes
main_api_router = APIRouter()
moderation_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(business_funcs_router, prefix="/business_funcs", tags=["business_funcs"])

moderation_router.include_router(category_router, prefix="/category", tags=["category"])
moderation_router.include_router(product_router, prefix="/product", tags=["product"])

main_api_router.include_router(moderation_router, prefix="/moderation", tags=["moderation"])

app.include_router(main_api_router)
