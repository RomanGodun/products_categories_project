import uuid

from app.api.schemas.moderation.base import (
    CreateInstanceRec,
    ShowInstanceResp,
    UpdateInstanceRec,
)
from app.api.schemas.tuned_model import TunedModel


class CreateProductToCategoryRec(CreateInstanceRec):
    product_id: uuid.UUID
    category_id: uuid.UUID


class UpdateProductToCategoryRec(UpdateInstanceRec):
    product_id: uuid.UUID | None
    category_id: uuid.UUID | None


# resp
class ShowProductToCategoryResp(ShowInstanceResp):
    product_id: uuid.UUID | None
    category_id: uuid.UUID | None


class ShowProductToCategoryRespWF(TunedModel):
    instances: list[ShowProductToCategoryResp]
    not_found_ids: list[uuid.UUID]
