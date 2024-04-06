from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


from ..basemixin import Base


class Size(Base):
    __tablename__ = "sizes"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    back_length = Column(Numeric, nullable=True)
    sleeve_length = Column(Numeric, nullable=True)
    leg_length = Column(Numeric, nullable=True)
    size_eu_code = Column(String, nullable=True)
    size_uk_code = Column(String, nullable=True)
    size_us_code = Column(String, nullable=True)
    size_it_code = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    products = relationship("Product", back_populates="size")
