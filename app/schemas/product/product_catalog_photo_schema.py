from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class ProductsCatalogPhotoBase(BaseModel):
    products_catalog_uuid: UUID4
    product_uuid: UUID4
    showcase: bool = False


class ProductsCatalogPhotoCreate(ProductsCatalogPhotoBase):
    pass


class ProductsCatalogPhotoRead(ProductsCatalogPhotoBase):
    uuid: UUID4
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProductsCatalogPhotoUpdate(BaseModel):
    showcase: Optional[bool] = None
