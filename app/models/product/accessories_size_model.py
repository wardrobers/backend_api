from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, backref
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class AccessoriesSize(Base):
    __tablename__ = "accessories_size"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    product_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )

    # Relationship
    product = relationship(
        "Product", backref=backref("accessories_sizes", uselist=True)
    )
