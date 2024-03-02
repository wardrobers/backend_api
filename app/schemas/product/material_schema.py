from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class MaterialBase(BaseModel):
    name: Optional[str]


class MaterialRead(MaterialBase):
    uuid: UUID4
    name: Optional[str]
    product_type_uuid: UUID4
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    # Nested relationship, assuming you have a ProductRead Pydantic model defined
    products: list["ProductRead"] = []

    class Config:
        orm_mode = True
