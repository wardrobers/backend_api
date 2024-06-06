from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.base_model import Base


class UserPromotions(Base):
    __tablename__ = "user_promotions"

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    promotion_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("promotions_and_discounts.id"), nullable=False
    )
