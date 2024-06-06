from sqlalchemy import Boolean, Column, Numeric, String
from sqlalchemy.orm import relationship

from app.models import Base


class DeliveryOptions(Base):
    __tablename__ = "delivery_options"

    name = Column(String, nullable=False)
    cost = Column(Numeric, nullable=True)
    active = Column(Boolean, default=True)

    # Relationships
    shipping_details = relationship(
        "app.model.orders.logistics.shipping_details_model.ShippingDetails",
        backref="delivery_options",
    )
