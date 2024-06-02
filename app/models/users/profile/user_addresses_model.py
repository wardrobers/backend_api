from enum import Enum

from sqlalchemy import Column, ForeignKey, String, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
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
    shipping_details = relationship("ShippingDetails", back_populates="user_addresses")
    transactions = relationship("Transactions", back_populates="user_addresses")

    async def add_or_update_address(
        self, db_session: AsyncSession, address_details: dict, address_id: UUID = None
    ):
        """Adds a new address or updates an existing one for a user."""
        if address_id:
            # Update existing address
            await db_session.execute(
                update(UserAddresses)
                .where(UserAddresses.id == address_id)
                .values(**address_details)
            )
        else:
            # Add new address
            new_address = UserAddresses(**address_details, user_id=self.user_id)
            db_session.add(new_address)

        await db_session.commit()
