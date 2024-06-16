from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.base_model import Base


class UserBasket(Base):
    __tablename__ = "user_basket"

    count = Column(Integer, default=0)

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    sku_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_units.id"), nullable=False
    )
