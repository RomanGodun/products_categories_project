import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.actions.moderation_actions import ModerationActions
from app.api.schemas.moderation.base import (
    CreateInstanceResp,
    DeleteInstanceRec,
    DeleteInstanceResp,
    ShowInstanceRec,
    UpdateInstanceResp,
)
from app.api.schemas.moderation.product import (
    CreateProductRec,
    ShowProductRespWF,
    UpdateProductRec,
)
from app.config.config import logger
from app.database.models.buisiness_entities import Product
from app.database.session_utils import get_session

product_router = APIRouter()


@product_router.post("/create", response_model=CreateInstanceResp)
async def create(
    title: str = Query(description="Title of the product", max_length=100),
    flammable: bool = Query(description="flammble or not"),
    price: int = Query(description="price of the product", ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    **create entry in table Product**:
    """
    received_param = locals()
    del received_param["session"]

    logger.debug(received_param)
    try:
        return await ModerationActions(Product).create_(session, [Product(**received_param)])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.post("/multi_create", response_model=CreateInstanceResp)
async def multi_create(body: list[CreateProductRec], session: AsyncSession = Depends(get_session)):
    """
    **create entries in table Product**:
    """
    logger.debug(body)

    sqlqlch_models = []
    for pydantic_model in body:
        sqlqlch_models.append(Product.from_dto(pydantic_model))

    logger.debug(sqlqlch_models)
    try:
        return await ModerationActions(Product).create_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.put("/update", response_model=UpdateInstanceResp)
async def update(
    id: uuid.UUID = Query(description="id existing entry in table"),
    title: str | None = Query(description="Title of the product", max_length=100, default=None),
    flammable: bool | None = Query(description="flammble or not", default=None),
    price: int | None = Query(description="price of the product", default=None, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    **update entry in table Product**:
    """
    received_param = locals()
    del received_param["session"]

    logger.debug(received_param)
    try:
        return await ModerationActions(Product).update_(session, [Product(**received_param)])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.put("/multi_update", response_model=UpdateInstanceResp)
async def multi_update(body: list[UpdateProductRec], session: AsyncSession = Depends(get_session)):
    """
    **create entries in table Product**:
    """

    logger.debug(body)

    sqlqlch_models = []

    for pydantic_model in body:
        sqlqlch_models.append(Product.from_dto(pydantic_model))

    logger.debug(sqlqlch_models)
    try:
        return await ModerationActions(Product).update_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.delete("/delete", response_model=DeleteInstanceResp)
async def delete(
    id: uuid.UUID = Query(description="id existing entry in table"), session: AsyncSession = Depends(get_session)
):
    """
    **delete entry in table Product**:
    """
    try:
        return await ModerationActions(Product).delete_(session, uuids=[id])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.delete("/multi_delete", response_model=DeleteInstanceResp)
async def multi_delete(body: DeleteInstanceRec, session: AsyncSession = Depends(get_session)):
    """
    **delete entries in table Product**:
    """
    logger.debug(body)
    try:
        return await ModerationActions(Product).delete_(session, dict(body)["ids"])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.get("/show", response_model=ShowProductRespWF)
async def show(
    id: uuid.UUID = Query(description="id existing entry in table"), session: AsyncSession = Depends(get_session)
):
    """
    **show  entry in table Product**:
    """
    try:
        return await ModerationActions(Product).show_(session, uuids=[id])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_router.post("/multi_show", response_model=ShowProductRespWF)
async def multi_show(body: ShowInstanceRec, session: AsyncSession = Depends(get_session)):
    """
    **show entries in table Product**:
    """
    logger.debug(body)
    try:
        return await ModerationActions(Product).show_(session, dict(body)["ids"])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
