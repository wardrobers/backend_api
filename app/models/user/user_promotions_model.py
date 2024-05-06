from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base

class UserPromotions(Base):
    __tablename__ = 'user_promotions'

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    promotion_uuid = Column(UUID(as_uuid=True), ForeignKey('promotions_and_discounts.uuid'), nullable=False)

    # Relationships
    promotion = relationship("PromotionAndDiscount", backref="user_promotions")