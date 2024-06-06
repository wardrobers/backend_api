from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models import Base


class UserReviewsAndRatings(Base):
    __tablename__ = "user_reviews_and_ratings"

    rating = Column(Integer)
    review = Column(Text)

    # Foreign Keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
