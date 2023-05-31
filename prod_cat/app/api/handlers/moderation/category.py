import uuid
from typing import Literal

from app.api.actions.moderation.base import ModerationActions
from app.api.schemas.moderation.base import (CreateInstanceResp,
                                             DeleteInstanceRec,
                                             DeleteInstanceResp,
                                             ShowInstanceRec,
                                             UpdateInstanceResp)
from app.api.schemas.moderation.category import (CreateCategoryRec,
                                                 ShowCategoryRespWF,
                                                 UpdateCategoryRec)
from app.config.config import logger
from app.database.models.buisiness_entities import Category
from app.database.session_utils import get_session
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

category_router  = APIRouter()       


@category_router.post("/create", response_model=CreateInstanceResp)
async def create(
    title:str = Query(description="Title of the category", max_length=100),
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
        return await ModerationActions(Category).create_(session, [Category(**received_param)])
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
        return await ModerationActions(Category).create_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


    
@category_router.put("/update", response_model=UpdateInstanceResp)
async def update(
    id: uuid.UUID = Query(description="id existing entry in table"),
    title:str | None  = Query(description="Title of the category" , max_length=100, default=None),
    rars: Literal["0+", "6+", "12+", "16+", "18+"] | None = Query(description="Russian Age Rating System, RARS", default=None),
    session: AsyncSession = Depends(get_session)
):
    """
    **update entry in table Category**:
    """
    received_param = locals()
    del received_param["session"]
    
    logger.debug(received_param)
    try:
        return await ModerationActions(Category).update_(session, [Category(**received_param)])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
 
 
   
@category_router.put("/multi_update", response_model=UpdateInstanceResp)
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
        return await ModerationActions(Category).update_(session, sqlqlch_models)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    

@category_router.delete("/delete", response_model=DeleteInstanceResp)
async def delete(
    id: uuid.UUID = Query(description="id existing entry in table"),
    session: AsyncSession = Depends(get_session)
):
    """
    **delete entry in table Category**:
    """
    try:
        return await ModerationActions(Category).delete_(session, uuids=[id])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

  
    
@category_router.delete("/multi_delete", response_model=DeleteInstanceResp)
async def multi_delete(
    body: DeleteInstanceRec,
    session: AsyncSession = Depends(get_session)
):
    """
    **delete entries in table Category**:
    """
    logger.debug(body)
    try:
        return await ModerationActions(Category).delete_(session, dict(body)["ids"])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@category_router.get("/show", response_model=ShowCategoryRespWF)
async def show(
    id: uuid.UUID = Query(description="id existing entry in table"),
    session: AsyncSession = Depends(get_session)
):
    """
    **show  entry in table Category**:
    """
    try:
        return await ModerationActions(Category).show_(session, uuids=[id])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

  
    
@category_router.post("/multi_show", response_model=ShowCategoryRespWF)
async def multi_show(
    body: ShowInstanceRec,
    session: AsyncSession = Depends(get_session)
):
    """
    **show entries in table Category**:
    """
    logger.debug(body)
    try:
        return await ModerationActions(Category).show_(session, dict(body)["ids"])
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")