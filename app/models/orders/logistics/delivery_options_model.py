from sqlalchemy import Boolean, Column, Numeric, String
from sqlalchemy.orm import relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class DeliveryOptions(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "delivery_options"

    name = Column(String, nullable=False)
    cost = Column(Numeric, nullable=True)
    active = Column(Boolean, default=True)

    # Relationships
    shipping_details = relationship(
        "app.model.orders.logistics.shipping_details_model.ShippingDetails",
        backref="delivery_options",
    )
