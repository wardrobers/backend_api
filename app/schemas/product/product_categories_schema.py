from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from .models import Category, ProductCategory


class ProductCategoryBase(BaseModel):
    uuid: Optional[UUID4]
    product_catalog_uuid: UUID4
    category_uuid: UUID4
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    category: Optional[Category]


class ProductCategoryList(BaseModel):
    product_categories: list(ProductCategory)
