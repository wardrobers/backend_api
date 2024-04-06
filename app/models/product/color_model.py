from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


from ..basemixin import Base


class Color(Base):
    __tablename__ = "colors"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    product_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    color = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    products = relationship(
        "Product", back_populates="color"
    )