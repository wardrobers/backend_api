from typing import Optional

from pydantic import UUID4, BaseModel

# --- Size Systems ---


class SizeSystemBase(BaseModel):
    name: str
    description: Optional[str] = None


class SizeSystemCreate(SizeSystemBase):
    pass


class SizeSystemRead(SizeSystemBase):
    id: UUID4


class SizeSystemUpdate(SizeSystemBase):
    name: Optional[str] = None
    description: Optional[str] = None


# --- Resolving Forward References ---
SizeSystemRead.model_rebuild()