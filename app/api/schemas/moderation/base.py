import uuid
from datetime import datetime

from app.api.schemas.tuned_model import TunedModel


class CreateInstanceRec(TunedModel):  # base
    pass


class UpdateInstanceRec(TunedModel):  # base
    id: uuid.UUID


class DeleteInstanceRec(TunedModel):
    ids: list[uuid.UUID]


class ShowInstanceRec(TunedModel):
    ids: list[uuid.UUID]


class CreateInstanceResp(TunedModel):
    created_ids: list[uuid.UUID]


class UpdateInstanceResp(TunedModel):
    updated_ids: list[uuid.UUID]
    not_found_ids: list[uuid.UUID]


class DeleteInstanceResp(TunedModel):
    deleted_ids: list[uuid.UUID]
    not_found_ids: list[uuid.UUID]


class ShowInstanceResp(TunedModel):  # base
    id: uuid.UUID
    created_at: datetime
    edited_at: datetime
