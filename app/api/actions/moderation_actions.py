from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.moderation.base import (
    CreateInstanceResp,
    DeleteInstanceResp,
    UpdateInstanceResp,
)
from app.api.schemas.moderation.category import ShowCategoryResp, ShowCategoryRespWF
from app.api.schemas.moderation.product import ShowProductResp, ShowProductRespWF
from app.api.schemas.moderation.product_to_category import (
    ShowProductToCategoryResp,
    ShowProductToCategoryRespWF,
)
from app.config.config import logger
from app.database.dals.base_model_dal import BaseModelDAL
from app.database.models.base import Base
from app.database.models.buisiness_entities import Category, Product, ProductToCategory

MATCHING_MODELS_SHEMES = {
    Category: {"show_resp": ShowCategoryResp, "show_resp_wf": ShowCategoryRespWF},
    Product: {"show_resp": ShowProductResp, "show_resp_wf": ShowProductRespWF},
    ProductToCategory: {"show_resp": ShowProductToCategoryResp, "show_resp_wf": ShowProductToCategoryRespWF},
}


class ModerationActions:
    def __init__(self, model: Base):
        self.model = model

        self.show_resp = MATCHING_MODELS_SHEMES[model]["show_resp"]
        self.show_resp_wf = MATCHING_MODELS_SHEMES[model]["show_resp_wf"]

    async def create_(self, session: AsyncSession, instances: list[Base]) -> BaseModel:
        refreshed_instances = await BaseModelDAL(session, self.model).create(instances)
        logger.debug(refreshed_instances)
        return CreateInstanceResp(created_ids=[instance.id for instance in refreshed_instances])

    async def update_(self, session: AsyncSession, instances: list[Base]) -> BaseModel:
        resived_instances = await BaseModelDAL(session, self.model).update(instances)
        logger.debug(resived_instances)

        done_insts = []
        failed_insts = []

        for i, resived_instance in enumerate(resived_instances):
            if resived_instance:
                done_insts.append(resived_instance.id)
            else:
                failed_insts.append(instances[i].id)

        return UpdateInstanceResp(updated_ids=done_insts, not_found_ids=failed_insts)

    async def delete_(self, session: AsyncSession, uuids: list[UUID]) -> BaseModel:
        resived_instances = await BaseModelDAL(session, self.model).delete(uuids)
        logger.debug(resived_instances)

        done_ids = {instance.id for instance in resived_instances}
        failed_ids = set(uuids).difference(done_ids)

        return DeleteInstanceResp(deleted_ids=list(done_ids), not_found_ids=list(failed_ids))

    async def show_(self, session: AsyncSession, uuids: UUID) -> BaseModel:
        resived_instances = await BaseModelDAL(session, self.model).get(uuids)
        logger.debug(resived_instances)

        done_ids = {instance.id for instance in resived_instances}
        failed_ids = set(uuids).difference(done_ids)

        return self.show_resp_wf(
            instances=[self.show_resp(**instance.as_dict(drop_base_fields=False)) for instance in resived_instances],
            not_found_ids=list(failed_ids),
        )
