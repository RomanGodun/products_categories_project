from app.api.schemas.moderation.base import (CreateInstanceRec,
                                             GetInstanceByIdResp,
                                             UpdateInstanceRec)
from app.api.schemas.base_tuned_model import TunedModel
from app.database.models.buisiness_entities import RARS
from fastapi import HTTPException
from pydantic import validator



class CreateCategoryRec(CreateInstanceRec):
    title: str
    rars: str | None
    
    @validator("title")
    def validate_title(cls, value):
        if not (1 <= len(value) <= 100):
            raise HTTPException(
                status_code=422, detail="The title must be less than 100 characters and more than 1"
            )
        return value
    
    @validator("rars")
    def validate_rars(cls, value):
        if value not in RARS:
            raise HTTPException(
                status_code=422, detail=f"The rars value must be in {RARS}"
            )
        return value


   
class UpdateCategoryRec(UpdateInstanceRec):
    title: str
    rars: str
    
    @validator("title")
    def validate_title(cls, value):
        if not (1 <= len(value) <= 100):
            raise HTTPException(
                status_code=422, detail="The title must be less than 100 characters and more than 1"
            )
        return value
    
    @validator("rars")
    def validate_rars(cls, value):
        if value not in RARS:
            raise HTTPException(
                status_code=422, detail=f"The rars value must be in {RARS}"
            )
        return value

# resp
class GetCategoryByIdResp(GetInstanceByIdResp):
    title: str
    rars: str