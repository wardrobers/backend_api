from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import mapped_column

from app.repositories.common import Base, BaseMixin


class Sizing(Base, BaseMixin):
    __tablename__ = "sizing"

    label = Column(String, nullable=False)
    measurements = Column(JSON)

    # Foreign keys
    variant_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("variants.id"), nullable=False
    )
    size_system_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("size_systems.id"), nullable=False
    )
