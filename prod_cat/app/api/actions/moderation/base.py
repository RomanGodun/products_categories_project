from uuid import UUID

from app.api.schemas.moderation.base import (CreateInstanceResp,
                                             DeleteInstanceResp,
                                             UpdateInstanceResp)
from app.config.config import logger
from app.database.dals.base_model_dal import BaseModelDAL
from app.database.models.base import Base
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import logger

class ModerationActions:
    def __init__(self, model:Base, get_by_id_resp: BaseModel):
        self.model = model
        self.get_by_id_resp = get_by_id_resp
        
        
    async def create_(self, session: AsyncSession, instances:list[Base]) -> BaseModel:
            refreshed_instances = await BaseModelDAL(session, self.model).create(instances)
            logger.debug(refreshed_instances)
            return CreateInstanceResp(created_instances_ids=[instance.id for instance in refreshed_instances])


    async def update_(self, session: AsyncSession, instances:list[Base]) -> BaseModel:
            refreshed_instances = await BaseModelDAL(session, self.model).update(instances)
            logger.debug(refreshed_instances)
            return UpdateInstanceResp(updated_instances_ids=[instance.id for instance in refreshed_instances])
       
        
    async def delete_(self, session: AsyncSession, uuid_: UUID) -> BaseModel:
            instance_id = await BaseModelDAL(session, self.model).delete(uuid_)
            logger.debug(instance_id)
            return DeleteInstanceResp(deleted_instance_id=instance_id)
     
     
    async def get_by_id_(self, session: AsyncSession, uuid_: UUID) -> BaseModel:
            instance = await BaseModelDAL(session, self.model).get(uuid_)
            logger.debug(instance)
            return self.get_by_id_resp(**instance.as_dict(drop_base_fields=False))
    