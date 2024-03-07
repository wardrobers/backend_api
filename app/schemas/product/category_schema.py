from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str


class CategoryRead(CategoryBase):
    uuid: UUID4
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str = Field(..., example="Summer Collection")

    class Config:
        schema_extra = {"example": {"name": "Summer Collection"}}


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Winter Collection")

    class Config:
        schema_extra = {"example": {"name": "Winter Collection"}}
