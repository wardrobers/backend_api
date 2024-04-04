from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, mapped_column
from sqlalchemy.sql import func


from ..basemixin import Base


class Category(Base):
    __tablename__ = "categories"
    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
    # Relationship back to Product
    products = relationship(
        "Product", secondary="product_categories", back_populates="categories"
    )
