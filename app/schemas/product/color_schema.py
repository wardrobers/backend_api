from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class ColorBase(BaseModel):
    color: Optional[str] = Field(None, max_length=255)


class ColorCreate(ColorBase):
    pass  # No additional fields for creation, can be extended if necessary


class ColorRead(BaseModel):
    uuid: UUID4
    color: Optional[str] = Field(None, max_length=255)
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ColorUpdate(BaseModel):
    color: Optional[str] = Field(None, max_length=255)
    # This allows partial updates, only include fields that can be updated


# Example for a specialized model, if needed, e.g., for filtering by creation date
class ColorFilter(BaseModel):
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
