from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, mapped_column
from sqlalchemy.sql import func


from ..basemixin import Base


class Category(Base):
    __tablename__ = "categories"
    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    product_type_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("product_types.uuid")
    )
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
    # Relationships
    product_type = relationship("ProductType", back_populates="categories")
    category_for_user = relationship("CategoryForUser", back_populates="category")
