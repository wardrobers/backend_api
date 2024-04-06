from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, mapped_column, relationship
from sqlalchemy.sql import func

from ..basemixin import Base


class Brand(Base):
    __tablename__ = "brands"
    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    products = relationship("Product", back_populates="brand")
    products_catalog = relationship("ProductsCatalog", back_populates="brand")
