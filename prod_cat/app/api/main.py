from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from app.api.handlers.business_funcs import business_funcs_router
from app.api.handlers.moderation.category import category_router
from app.database.session_utils import connect, disconnect


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect()
    yield
    disconnect()

app = FastAPI(lifespan=lifespan)

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(business_funcs_router, prefix="/business_funcs", tags=["business_funcs"])
main_api_router.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(main_api_router)
