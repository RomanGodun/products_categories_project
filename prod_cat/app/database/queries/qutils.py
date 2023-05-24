from enum import Enum, auto

from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import logger

# async def run_some_sql(async_session: async_sessionmaker[AsyncSession]) -> None:
#     async with async_session() as session:
#         session.add(SomeObject(data="object"))
#         session.add(SomeOtherObject(name="other object"))
#         await session.commit()

class READ_TYPE(int, Enum):
    ONE_VALUE = auto()
    FIRST_ROW = auto()
    ALL = auto()

   
async def read(query, session: AsyncSession , read_type:READ_TYPE = READ_TYPE.ALL) -> list:
    logger.debug(f"start execute \n {query}")
    
    result = await session.execute(query)
    
    logger.debug(read_type)
    
    if read_type == READ_TYPE.ONE_VALUE:
        return result.scalar()
    
    elif read_type == READ_TYPE.FIRST_ROW:
        return result.first()
            
    elif read_type == READ_TYPE.ALL:
        return result.all()
    
    

