from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from .category_schema import CategoryBase


class ProductCategoryBase(BaseModel):
    uuid: Optional[UUID4]
    products_catalog_id: UUID4
    category_id: UUID4
    created_at: datetime
    deleted_at: Optional[datetime]
    category: Optional[CategoryBase]


class ProductCategoryList(BaseModel):
    product_categories: list[ProductCategoryBase]
