from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class ProductStatusBase(BaseModel):
    code: str
    name: str


class ProductStatusCreate(ProductStatusBase):
    pass  # This model is used when creating a new product status, all fields are required here.


class ProductStatusRead(ProductStatusBase):
    uuid: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models


class ProductStatusUpdate(BaseModel):
    code: Optional[str]
    name: Optional[str]
