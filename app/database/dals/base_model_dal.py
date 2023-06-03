from itertools import chain
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.config import logger
from app.database.dals.base_dal import BaseDAL
from app.database.models.base import Base


class BaseModelDAL(BaseDAL):
    """Data Access Layer for operating tables info"""

    def __init__(self, async_session: AsyncSession, model: Base):
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

    async def update(
        self,
        instances: list[Base],
        create_uuid_if_not_exist: bool = False,
        return_updated_inst: bool = True,
    ) -> list[Base | None]:

        logger.debug(instances)

        if create_uuid_if_not_exist:

            async with self.async_session.begin():
                for instance in instances:
                    await self.async_session.merge(instance)

            return instances

        values = [instance.as_dict(drop_base_fields=False, wo_none=True) for instance in instances]

        # bulk update not support .returning -
        # https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#bulk-update
        if return_updated_inst:

            updated_insts = []

            async with self.async_session.begin():
                for value in values:
                    uuid_ = value.pop("id")

                    query = update(self.Model).where(self.Model.id == uuid_).values(value).returning(self.Model)

                    res = await self.async_session.execute(query)
                    row = res.first()

                    updated_insts.append(row[0] if row else None)

                return updated_insts

        else:
            async with self.async_session.begin():
                res = await self.async_session.execute(update(self.Model), values)
            return list(chain(*res))

    async def delete(
        self,
        uuids: list[UUID],
    ) -> list[Base | None]:

        logger.debug(uuids)

        query = delete(self.Model).where(self.Model.id.in_(uuids)).returning(self.Model)

        async with self.async_session.begin():
            res = await self.async_session.execute(query)

        return list(chain(*res.all()))

    async def get(self, uuids: UUID) -> Base | None:
        query = select(self.Model).where(self.Model.id.in_(uuids))

        async with self.async_session.begin():
            res = await self.async_session.execute(query)

        return list(chain(*res.all()))
