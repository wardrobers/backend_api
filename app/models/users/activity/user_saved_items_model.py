from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.models.base_model import Base


class UserSavedItems(Base):
    __tablename__ = "user_saved_items"

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    variant_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("variants.id"), nullable=False
    )
