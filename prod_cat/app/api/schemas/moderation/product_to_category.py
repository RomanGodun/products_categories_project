import uuid
from app.api.schemas.moderation.base import (CreateInstanceRec,
                                             GetInstanceByIdResp,
                                             UpdateInstanceRec)

#rec
class CreateProductToCategoryRec(CreateInstanceRec):
    product_id: uuid.UUID
    category_id: uuid.UUID
    
class UpdateProductToCategoryRec(UpdateInstanceRec):
    product_id: uuid.UUID
    category_id: uuid.UUID

# resp
class GetProductToCategoryByIdResp(GetInstanceByIdResp):
    product_id: uuid.UUID
    category_id: uuid.UUID