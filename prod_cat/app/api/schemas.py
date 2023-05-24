from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True
        
        
class ProductsSchema(TunedModel):
    product: str
    categories: list | None


class CategoriesSchema(TunedModel):
    category: str
    products: list | None


class ProductsToCategoriesSchema(TunedModel):
    product: str
    category: str