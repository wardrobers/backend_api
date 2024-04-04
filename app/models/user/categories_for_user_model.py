from sqlalchemy import ForeignKey, JSON, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func


from ..basemixin import Base


class CategoryForUser(Base):
    __tablename__ = "categories_for_user"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    category_uuid = Column(UUID(as_uuid=True), ForeignKey("categories.uuid"))
    coefficient = Column(String)
    raw = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    user = relationship("User", back_populates="categories_for_user")
    category = relationship("Category", back_populates="categories_for_user")
