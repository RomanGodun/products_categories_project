from app.api.schemas.tuned_model import TunedModel


class ProductsSchema(TunedModel):
    product: str
    categories: list | None


class CategoriesSchema(TunedModel):
    category: str
    products: list | None


class ProductsToCategoriesSchema(TunedModel):
    product: str
    category: str
