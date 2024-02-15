from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

from .category_schema import CategoryRead
from .material_schema import MaterialRead


class ProductRead(BaseModel):
    uuid: UUID4
    status_code: str
    product_catalog_uuid: UUID4
    color_uuid: UUID4
    number: str
    name: Optional[str] = None
    article: Optional[str] = None
    size_uuid: UUID4
    usage_count: int
    usage_seconds: int
    factory_number: Optional[str] = None
    base_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    categories: list[CategoryRead] = []
    materials: list[MaterialRead] = []

    class Config:
        orm_mode = True


# Update forward refs if needed
ProductRead.update_forward_refs()