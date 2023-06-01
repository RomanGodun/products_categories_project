import uuid

from fastapi import HTTPException
from pydantic import validator

from app.api.schemas.moderation.base import (
    CreateInstanceRec,
    ShowInstanceResp,
    UpdateInstanceRec,
)
from app.api.schemas.tuned_model import TunedModel


class CreateProductRec(CreateInstanceRec):
    title: str
    flammable: bool
    price: int

    @validator("title")
    def validate_title(cls, value):
        if not (1 <= len(value) <= 100):
            raise HTTPException(status_code=422, detail="The title must be less than 100 characters and more than 1")
        return value

    @validator("price")
    def validate_name(cls, value):
        if value < 0:
            raise HTTPException(status_code=422, detail="Price must be more than 0")
        return value


class UpdateProductRec(UpdateInstanceRec):
    title: str | None
    flammable: bool | None
    price: int | None

    @validator("title")
    def validate_title(cls, value):
        if not (1 <= len(value) <= 100):
            raise HTTPException(status_code=422, detail="The title must be less than 100 characters and more than 1")
        return value

    @validator("price")
    def validate_name(cls, value):
        if value < 0:
            raise HTTPException(status_code=422, detail="Price must be more than 0")
        return value


# resp
class ShowProductResp(ShowInstanceResp):
    title: str
    flammable: bool
    price: int


class ShowProductRespWF(TunedModel):
    instances: list[ShowProductResp]
    not_found_ids: list[uuid.UUID]
