from typing import Optional

from pydantic import UUID4, BaseModel

# --- Materials ---


class MaterialBase(BaseModel):
    name: str
    category_id: UUID4


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(MaterialBase):
    id: UUID4


class MaterialUpdate(MaterialBase):
    name: Optional[str] = None
