from typing import Union
from uuid import UUID

from app.database.models.base import Base
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dals.base import BaseDAL


class BaseModelDAL(BaseDAL):
    """Data Access Layer for operating tables info"""

    def __init__(self, async_session: AsyncSession, model:Base):
        super.__init__(async_session)
        self.Model = model

    async def create(
        self,
        **fields,
    ) -> Base:
        new_obj = self.Model(**fields)
        
        await self.async_session.add(new_obj)
        
        return new_obj
    
    
    async def multi_create(
        self,
        objects: list[Base],
    ) -> None:
        await self.async_session.add_all(objects)


    async def update(self, uuid_: UUID, **fields) -> Union[UUID, None]:
        query = (
            update(self.Model)
            .where(self.Model.id == uuid_)
            .values(fields)
            .returning(self.Model.id)
        )
        
        return await self.async_session.scalar(query)
        
           
    async def delete(self, uuid_: UUID) -> Union[UUID, None]:
        query = (
            delete(self.Model)
            .where(self.Model.id == uuid_)
            .returning(self.Model.id)
        )
        
        return await self.async_session.scalar(query)


    async def get(self, uuid_: UUID) -> Union[Base, None]:
        return await self.async_session.get(self.Model,uuid_)
    
    
    
    
        

    