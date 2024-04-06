from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class CatalogProductTypeBase(BaseModel):
    product_type_uuid: UUID
    products_catalog_uuid: UUID


class CatalogProductTypeCreate(CatalogProductTypeBase):
    pass


class CatalogProductTypeRead(CatalogProductTypeBase):
    uuid: UUID
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CatalogProductTypeUpdate(BaseModel):
    product_type_uuid: Optional[UUID] = None
    products_catalog_uuid: Optional[UUID] = None

    class Config:
        from_attributes = True
