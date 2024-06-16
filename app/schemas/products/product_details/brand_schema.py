from typing import Optional

from pydantic import UUID4, BaseModel

# --- Products ---


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class BrandRead(BrandBase):
    id: UUID4


class BrandUpdate(BrandBase):
    name: Optional[str] = None
