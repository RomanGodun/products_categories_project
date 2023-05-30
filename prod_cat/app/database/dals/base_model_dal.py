from typing import Union
from uuid import UUID

from app.database.models.base import Base
from sqlalchemy import delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dals.base_dal import BaseDAL
from app.config.config import logger




class BaseModelDAL(BaseDAL):
    """Data Access Layer for operating tables info"""

    def __init__(self, async_session: AsyncSession, model:Base):
        super().__init__(async_session)
        self.Model = model
    
    
    async def create(
        self,
        instances: list[Base],
    ) -> list[Base]:
        
        logger.debug(instances)
        
        async with self.async_session.begin():
            # add и add_all ломается с директивой async TODO: изучить
            self.async_session.add_all(instances)
            await self.async_session.flush()
            
        return instances


    # async def update(self, uuid_: UUID, fields:dict) -> UUID | None:
    async def update(
        self,
        instances: list[Base],
    ) -> list[Base]:
        
        # query = (
        #     update(self.Model)
        #     .where(self.Model.id == uuid_)
        #     .values(fields)
        #     .returning(self.Model.id)
        # )
        logger.info(instances)
        
        async with self.async_session.begin():
            for instance in instances:
                await self.async_session.merge(instance)
            
        logger.debug(instances)
            
        return instances
        
           
    async def delete(self, uuid_: UUID) -> UUID | None:
        query = (
            delete(self.Model)
            .where(self.Model.id == uuid_)
            .returning(self.Model.id)
        )
        
        async with self.async_session.begin():
            return await self.async_session.scalar(query)


    async def get(self, uuid_: UUID) -> Base | None:
        return await self.async_session.get(self.Model,uuid_)
    
    
    
    
        

    