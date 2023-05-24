from sqlalchemy import select, func
from app.database.models.product_logic import Product, Category, ProductToCategory

select_product_categories = (
        select(
                Product.product_name.label("product"),
                func.array_agg(
                    Category.category_name
                ).label("categories")
        )
        .join_from(Product, ProductToCategory)
        .join(Category)
        .group_by(Product.product_name)
        .order_by(Product.product_name)
)

select_category_products = (
        select(
                Category.category_name.label("category"),
                func.array_agg(
                    Product.product_name
                ).label("products")
        )
        .join_from(Category, ProductToCategory)
        .join(Product)
        .group_by(Category.category_name)
        .order_by(Category.category_name)
)


select_product_category_pairs = (
        select(
                Product.product_name.label("product"),
                Category.category_name.label("category")
        )
        .join_from(Product, ProductToCategory)
        .join(Category)
        .order_by(Product.product_name)
)

