
import uuid
from app.api.schemas.base_tuned_model import TunedModel

class CreateInstanceRec(TunedModel): #base
    pass
    
class UpdateInstanceRec(TunedModel): #base
    id: uuid.UUID

class DeleteInstanceRec(TunedModel):
    id: uuid.UUID

class GetInstanceByIdRec(TunedModel):
    id: uuid.UUID



class CreateInstanceResp(TunedModel):
    created_instances_ids: list[uuid.UUID]

class UpdateInstanceResp(TunedModel):
    updated_instances_ids: list[uuid.UUID]

class DeleteInstanceResp(TunedModel):
    deleted_instance_id: uuid.UUID
    
class GetInstanceByIdResp(TunedModel): #base
    id: uuid.UUID
    
    
    
    

# CreateInstanceRec,
# CreateInstanceResp,
# DeleteInstanceRec,
# DeleteInstanceResp,
# GetInstanceByIdRec,
# GetInstanceByIdResp,
# TitleValidationMixin,
# UpdateInstanceRec,
# UpdateInstanceResp
    