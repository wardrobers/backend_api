from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime



class ProductPhotoBase(BaseModel):
    product_uuid: UUID4
    showcase: Optional[bool] = False


class ProductPhotoCreate(ProductPhotoBase):
    pass  # No additional fields needed for creation; can extend if necessary.


class ProductPhotoRead(BaseModel):
    uuid: UUID4
    product_uuid: UUID4
    showcase: bool
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProductPhotoUpdate(BaseModel):
    showcase: Optional[bool] = None
    # This allows partial updates, only include fields that can be updated
