
from typing import Generator

from app.config.config import db_url
from app.database.models.base import Base
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)



engine = create_async_engine(db_url, echo=True)
ASYNC_SMAKER = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> Generator[AsyncSession, None, None]:
    """Dependency for getting async session"""
    async with ASYNC_SMAKER() as session:
        yield session

async def connect() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

async def disconnect() -> None:
    if engine:
        await engine.dispose()