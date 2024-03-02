from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class BrandRead(BrandBase):
    uuid: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    # You can add fields here that can be updated
