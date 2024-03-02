from sqlalchemy import Column, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    product_uuid = Column(UUID(as_uuid=True), ForeignKey("products.uuid"))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    price = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
    # Relationships
    user = relationship("User", back_populates="orders")
    product = relationship("Product")
