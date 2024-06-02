from enum import Enum

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class AddressType(Enum):
    Shipping = "Shipping"
    Billing = "Billing"
    Both = "Both"


class UserAddresses(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "user_addresses"

    address_line1 = Column(String)
    address_line2 = Column(String, nullable=True)
    city = Column(String)
    country = Column(String)
    postal_code = Column(String)
    address_type = Column(SQLAEnum(AddressType))

    # Foreign Keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relationships
    shipping_details = relationship(
        "app.models.orders.logistics.shipping_details_model.ShippingDetails",
        back_populates="user_addresses",
    )
    transactions = relationship(
        "app.models.orders.payments.transactions_model.Transactions",
        back_populates="user_addresses",
    )
