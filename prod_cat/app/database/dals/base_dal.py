from enum import Enum, auto

from app.config.config import logger
from sqlalchemy.ext.asyncio import AsyncSession


class READ_TYPE(int, Enum):
    ONE_VALUE = auto()
    FIRST_ROW = auto()
    ALL = auto()
    
    
class BaseDAL:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session
        
    async def read(self, query, read_type:READ_TYPE = READ_TYPE.ALL) -> list:
        logger.debug(f"start execute \n {query}")
        
        result = await self.async_session.execute(query)
        
        logger.debug(read_type)
        
        if read_type == READ_TYPE.ONE_VALUE:
            return result.scalar()
        
        elif read_type == READ_TYPE.FIRST_ROW:
            return result.first()
                
        elif read_type == READ_TYPE.ALL:
            return result.all()
        
    
    async def multi_session_join(self):
        #TODO
        raise NotImplemented