from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.repositories.common import Base, BaseMixin


class UserBasket(Base, BaseMixin):
    __tablename__ = "user_basket"

    count = Column(Integer, default=1)

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stock_keeping_unit_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_units.id"), nullable=False
    )
