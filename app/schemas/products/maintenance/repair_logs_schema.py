from typing import Optional

from pydantic import BaseModel, UUID4, Field
from datetime import datetime


# --- RepairLogs ---

class RepairLogBase(BaseModel):
    description: Optional[str] = Field(None, description="Description of the repair work done.")
    cost: Optional[int] = Field(None, description="Cost of the repair.")
    repair_date: datetime = Field(..., description="The date when the repair was performed.")
    article_id: UUID4 = Field(..., description="The ID of the article that was repaired.")


class RepairLogCreate(RepairLogBase):
    pass


class RepairLogRead(RepairLogBase):
    id: UUID4

    class Config:
        orm_mode = True


class RepairLogUpdate(RepairLogBase):
    description: Optional[str] = Field(None, description="Description of the repair work done.")
    cost: Optional[int] = Field(None, description="Cost of the repair.")
    repair_date: Optional[datetime] = Field(None, description="The date when the repair was performed.")


# --- Resolving Forward References ---
RepairLogRead.model_rebuild()