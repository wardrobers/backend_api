from pydantic import BaseModel, UUID4, Field
from typing import Optional, Dict
from datetime import datetime


class CategoryForUserBase(BaseModel):
    coefficient: Optional[str] = None
    raw: Optional[Dict] = None


class CategoryForUserCreate(CategoryForUserBase):
    user_uuid: UUID4
    category_uuid: UUID4


class CategoryForUserRead(CategoryForUserBase):
    uuid: UUID4
    user_uuid: UUID4
    category_uuid: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryForUserUpdate(BaseModel):
    coefficient: Optional[str] = None
    raw: Optional[Dict] = None

    class Config:
        from_attributes = True
