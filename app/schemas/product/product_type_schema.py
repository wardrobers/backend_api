from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as UUIDType
from datetime import datetime


class ProductTypeBase(BaseModel):
    uuid: Optional[UUIDType]
    name: str


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeRead(ProductTypeBase):
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
