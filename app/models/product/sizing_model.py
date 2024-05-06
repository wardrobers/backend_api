from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base

class Sizing(Base):
    __tablename__ = "sizing"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    label = Column(String, nullable=False)
    measurements = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    variant_uuid = Column(UUID(as_uuid=True), ForeignKey('variants.uuid'), nullable=False)
    size_system_uuid = Column(UUID(as_uuid=True), ForeignKey('size_systems.uuid'), nullable=False)

    # Relationships
    variant = relationship("Variant", backref=backref("sizings", uselist=True))
    size_system = relationship("SizeSystem", backref=backref("sizings", uselist=True))