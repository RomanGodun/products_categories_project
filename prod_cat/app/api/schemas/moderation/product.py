from app.api.schemas.moderation.base import (CreateInstanceRec,
                                             GetInstanceByIdResp,
                                             TitleValidationMixin,
                                             UpdateInstanceRec)
from fastapi import HTTPException
from pydantic import validator


class PriceValidationMixin:
    price: str

    @validator("price")
    def validate_name(cls, value):
        if value < 1:
            raise HTTPException(
                status_code=422, detail="Price must be more than 1"
            )
        return value

#rec
class CreateProductRec(CreateInstanceRec, TitleValidationMixin, PriceValidationMixin):
    flammable: bool
      
class UpdateProductRec(UpdateInstanceRec, TitleValidationMixin, PriceValidationMixin):
    flammable: bool

#resp
class GetProductByIdResp(GetInstanceByIdResp, PriceValidationMixin):
    title: str
    flammable: bool
  

    
    
    

