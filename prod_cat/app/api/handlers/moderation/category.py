from app.api.actions.moderation.base import ModerationActions
from app.database.models.buisiness_entities import Product, Category, RARS

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import logger
from app.database.session_utils import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.moderation.category import CreateCategoryRec, GetCategoryByIdResp, UpdateCategoryRec
from app.api.schemas.moderation. base import CreateInstanceResp, UpdateInstanceResp
import uuid
from typing import List, Literal, Optional, Union, Annotated
from pydantic import parse_obj_as
from fastapi import FastAPI, Body, Query

category_router  = APIRouter()       


@category_router.post("/create", response_model=CreateInstanceResp)
async def create(
    title:str = Query(description="Title of the category", max_length=100,  min_length=1),
    rars: Literal["0+", "6+", "12+", "16+", "18+"] | None = Query(description="Russian Age Rating System, RARS", default=None),
    session: AsyncSession = Depends(get_session)
):
    """
    **create entry in table Category**:
    """
    received_param = locals()
    del received_param["session"]
    
    logger.debug(received_param)
    try:
        return await ModerationActions(Category, GetCategoryByIdResp).create_(session, [Category(**received_param)])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

  
    
@category_router.post("/multi_create", response_model=CreateInstanceResp)
async def multi_create(
    body: list[CreateCategoryRec],
    session: AsyncSession = Depends(get_session)
):
    """
    **create entries in table Category**:
    """
    
    logger.debug(body)
    
    sqlqlch_models = []
    
    for pydantic_model in body:
        sqlqlch_models.append(Category.from_dto(pydantic_model))
    
    logger.debug(sqlqlch_models)
    try:
        return await ModerationActions(Category, GetCategoryByIdResp).create_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
@category_router.post("/update", response_model=UpdateInstanceResp)
async def update(
    id: uuid.UUID,
    body: list[UpdateCategoryRec],
    session: AsyncSession = Depends(get_session)
):
    """
    **create entries in table Category**:
    """
    
    logger.debug(body)
    
    sqlqlch_models = []
    
    for pydantic_model in body:
        sqlqlch_models.append(Category.from_dto(pydantic_model))
    
    logger.debug(sqlqlch_models)
    
    try:
        return await ModerationActions(Category, GetCategoryByIdResp).update_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
   
@category_router.post("/multi_update", response_model=UpdateInstanceResp)
async def multi_update(
    body: list[UpdateCategoryRec],
    session: AsyncSession = Depends(get_session)
):
    """
    **create entries in table Category**:
    """
    
    logger.debug(body)
    
    sqlqlch_models = []
    
    for pydantic_model in body:
        sqlqlch_models.append(Category.from_dto(pydantic_model))
    
    logger.debug(sqlqlch_models)
    
    try:
        return await ModerationActions(Category, GetCategoryByIdResp).update_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")