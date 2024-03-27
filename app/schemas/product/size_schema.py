from pydantic import BaseModel, UUID4
from typing import Optional
import datetime


class SizeBase(BaseModel):
    back_length: Optional[float] = None
    sleeve_length: Optional[float] = None
    leg_length: Optional[float] = None
    size_eu_code: Optional[str] = None
    size_uk_code: Optional[str] = None
    size_us_code: Optional[str] = None
    size_it_code: Optional[str] = None


class SizeCreate(SizeBase):
    # Assuming all fields are required when creating a new size entry
    back_length: float
    sleeve_length: float
    leg_length: float
    size_eu_code: str
    size_uk_code: str
    size_us_code: str
    size_it_code: str


class SizeRead(SizeBase):
    uuid: UUID4
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class SizeUpdate(BaseModel):
    # All fields are optional for updates
    back_length: Optional[float] = None
    sleeve_length: Optional[float] = None
    leg_length: Optional[float] = None
    size_eu_code: Optional[str] = None
    size_uk_code: Optional[str] = None
    size_us_code: Optional[str] = None
    size_it_code: Optional[str] = None
