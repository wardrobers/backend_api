from typing import Optional

from pydantic import BaseModel, UUID4, Field
from datetime import datetime


# --- CleaningLogs ---

class CleaningLogBase(BaseModel):
    article: str = Field(..., description="Article identifier (potentially redundant with article_id).")
    description: Optional[str] = Field(None, description="Description of the cleaning performed.")
    cost: Optional[int] = Field(None, description="Cost of the cleaning.")
    cleaning_date: datetime = Field(..., description="The date when the cleaning was performed.")
    article_id: UUID4 = Field(..., description="The ID of the article that was cleaned.")


class CleaningLogCreate(CleaningLogBase):
    pass


class CleaningLogRead(CleaningLogBase):
    id: UUID4

    class Config:
        from_attributes = True


class CleaningLogUpdate(CleaningLogBase):
    article: Optional[str] = Field(None, description="Article identifier (potentially redundant with article_id).")
    description: Optional[str] = Field(None, description="Description of the cleaning performed.")
    cost: Optional[int] = Field(None, description="Cost of the cleaning.")
    cleaning_date: Optional[int] = Field(None, description="The date when the cleaning was performed.")


# --- Resolving Forward References ---
CleaningLogRead.model_rebuild()