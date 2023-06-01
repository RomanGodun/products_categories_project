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
from app.api.schemas.moderation.product_to_category import (
    CreateProductToCategoryRec,
    ShowProductToCategoryRespWF,
    UpdateProductToCategoryRec,
)
from app.config.config import logger
from app.database.models.buisiness_entities import ProductToCategory
from app.database.session_utils import get_session

product_to_category_router = APIRouter()


@product_to_category_router.post("/create", response_model=CreateInstanceResp)
async def create(
    product_id: uuid.UUID = Query(description="id of the product"),
    category_id: uuid.UUID = Query(description="id of the category"),
    session: AsyncSession = Depends(get_session),
):
    """
    **create entry in table ProductToCategory**:
    """
    received_param = locals()
    del received_param["session"]

    logger.debug(received_param)
    try:
        return await ModerationActions(ProductToCategory).create_(session, [ProductToCategory(**received_param)])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_to_category_router.post("/multi_create", response_model=CreateInstanceResp)
async def multi_create(body: list[CreateProductToCategoryRec], session: AsyncSession = Depends(get_session)):
    """
    **create entries in table ProductToCategory**:
    """
    logger.debug(body)

    sqlqlch_models = []
    for pydantic_model in body:
        sqlqlch_models.append(ProductToCategory.from_dto(pydantic_model))

    logger.debug(sqlqlch_models)
    try:
        return await ModerationActions(ProductToCategory).create_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_to_category_router.put("/update", response_model=UpdateInstanceResp)
async def update(
    id: uuid.UUID = Query(description="id existing entry in table"),
    product_id: uuid.UUID | None = Query(description="id of the product", default=None),
    category_id: uuid.UUID | None = Query(description="id of the category", default=None),
    session: AsyncSession = Depends(get_session),
):
    """
    **update entry in table ProductToCategory**:
    """
    received_param = locals()
    del received_param["session"]

    logger.debug(received_param)
    try:
        return await ModerationActions(ProductToCategory).update_(session, [ProductToCategory(**received_param)])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_to_category_router.put("/multi_update", response_model=UpdateInstanceResp)
async def multi_update(body: list[UpdateProductToCategoryRec], session: AsyncSession = Depends(get_session)):
    """
    **create entries in table ProductToCategory**:
    """

    logger.debug(body)

    sqlqlch_models = []

    for pydantic_model in body:
        sqlqlch_models.append(ProductToCategory.from_dto(pydantic_model))

    logger.debug(sqlqlch_models)
    try:
        return await ModerationActions(ProductToCategory).update_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_to_category_router.delete("/delete", response_model=DeleteInstanceResp)
async def delete(
    id: uuid.UUID = Query(description="id existing entry in table"), session: AsyncSession = Depends(get_session)
):
    """
    **delete entry in table ProductToCategory**:
    """
    try:
        return await ModerationActions(ProductToCategory).delete_(session, uuids=[id])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_to_category_router.delete("/multi_delete", response_model=DeleteInstanceResp)
async def multi_delete(body: DeleteInstanceRec, session: AsyncSession = Depends(get_session)):
    """
    **delete entries in table ProductToCategory**:
    """
    logger.debug(body)
    try:
        return await ModerationActions(ProductToCategory).delete_(session, dict(body)["ids"])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_to_category_router.get("/show", response_model=ShowProductToCategoryRespWF)
async def show(
    id: uuid.UUID = Query(description="id existing entry in table"), session: AsyncSession = Depends(get_session)
):
    """
    **show  entry in table ProductToCategory**:
    """
    try:
        return await ModerationActions(ProductToCategory).show_(session, uuids=[id])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@product_to_category_router.post("/multi_show", response_model=ShowProductToCategoryRespWF)
async def multi_show(body: ShowInstanceRec, session: AsyncSession = Depends(get_session)):
    """
    **show entries in table ProductToCategory**:
    """
    logger.debug(body)
    try:
        return await ModerationActions(ProductToCategory).show_(session, dict(body)["ids"])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
