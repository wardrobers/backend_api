from typing import Optional

from pydantic import UUID4, BaseModel

# --- Colors ---


class ColorBase(BaseModel):
    name: str


class ColorCreate(ColorBase):
    pass


class ColorRead(ColorBase):
    id: UUID4


class ColorUpdate(ColorBase):
    name: Optional[str] = None
