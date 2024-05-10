from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, backref
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class PeerToPeerLogistics(Base):
    __tablename__ = "peer_to_peer_logistics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

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
        "User",
        foreign_keys=[lender_user_id],
        backref=backref("lender_logistics", uselist=True),
    )
    renter_user = relationship(
        "User",
        foreign_keys=[renter_user_id],
        backref=backref("renter_logistics", uselist=True),
    )
    order_item = relationship("OrderItem", backref=backref("logistics", uselist=True))
    shipping_detail = relationship(
        "ShippingDetail", backref=backref("logistics", uselist=True)
    )
