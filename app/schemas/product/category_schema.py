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
