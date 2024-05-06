from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base

class UserReviewsAndRatings(Base):
    __tablename__ = 'user_reviews_and_ratings'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    rating = Column(Integer)
    review = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Foreign Keys
    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    product_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('products.uuid'), nullable=False)