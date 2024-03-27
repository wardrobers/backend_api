from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

from .product_schema import ProductRead
from .material_schema import MaterialRead


class ProductMaterialBase(BaseModel):
    product_uuid: UUID4
    material_uuid: UUID4
    percent: Optional[int] = None


class ProductMaterialCreate(ProductMaterialBase):
    pass  # You may want to enforce all fields here, remove Optional if needed


class ProductMaterialRead(ProductMaterialBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductMaterialUpdate(BaseModel):
    percent: Optional[int] = None  # Only include fields that can be updated


class ProductMaterialReadWithDetails(ProductMaterialRead):
    product: Optional[ProductRead] = None
    material: Optional[MaterialRead] = None


# Don't forget to call update_forward_refs to resolve forward declarations
# ProductMaterialReadWithDetails.update_forward_refs()
