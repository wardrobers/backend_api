from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class CatalogProductTypeBase(BaseModel):
    product_type_uuid: UUID
    product_catalog_uuid: UUID


class CatalogProductTypeCreate(CatalogProductTypeBase):
    pass


class CatalogProductTypeRead(CatalogProductTypeBase):
    uuid: UUID
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CatalogProductTypeUpdate(BaseModel):
    product_type_uuid: Optional[UUID] = None
    product_catalog_uuid: Optional[UUID] = None

    class Config:
        orm_mode = True
