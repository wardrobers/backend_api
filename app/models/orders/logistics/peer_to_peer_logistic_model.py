from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, mapped_column, relationship

from app.models.base_model import Base
from app.models.orders.core.order_items_model import OrderItems
from app.models.orders.logistics.shipping_details_model import ShippingDetails
from app.models.users import Users


class PeerToPeerLogistics(Base):
    __tablename__ = "peer_to_peer_logistics"

    # Foreign Keys
    lender_user_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    renter_user_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    item_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("order_items.id"), nullable=False
    )
    shipping_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("shipping_details.id"), nullable=False
    )

    # Relationships
    lender_user = relationship(
        "Users",
        foreign_keys=[lender_user_id],
        backref=backref("lender_logistics", uselist=True),
    )
    renter_user = relationship(
        "Users",
        foreign_keys=[renter_user_id],
        backref=backref("renter_logistics", uselist=True),
    )
    order_item = relationship(
        "OrderItems",
        backref=backref("logistics", uselist=True),
    )
    shipping_detail = relationship(
        "ShippingDetails",
        backref=backref("logistics", uselist=True),
    )
