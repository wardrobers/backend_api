from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class Orders(Base):
    __tablename__ = "orders"

    total_price = Column(Numeric, nullable=False)
    total_delivery_price = Column(Numeric, nullable=False)
    comment = Column(String, nullable=True)

    # Foreign keys
    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    status_code = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("order_status.id"),
        nullable=False,
    )

    # Relationships
    transactions = relationship(
        "app.models.orders.Transactions", backref="orders"
    )
    order_items = relationship(
        "app.models.orders.OrderItems", backref="orders"
    )
    order_promotions = relationship(
        "app.models.promotions.OrderPromotions", backref="orders"
    )
