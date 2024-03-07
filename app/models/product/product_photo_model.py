from sqlalchemy import Column, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class ProductPhoto(Base):
    __tablename__ = "product_photos"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    product_uuid = Column(UUID(as_uuid=True), ForeignKey("products.uuid"))
    showcase = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)
