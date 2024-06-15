from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class Variants(Base):
    __tablename__ = "variants"

    name = Column(String, nullable=False)
    index = Column(Integer)

    # Foreign Keys
    product_id = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    sku_id = mapped_column(UUID(as_uuid=True), ForeignKey("stock_keeping_units.id"))
    color_id = mapped_column(UUID(as_uuid=True), ForeignKey("colors.id"))

    # Relationships
    sizing = relationship(
        "Sizing", backref="variants", cascade="all, delete-orphan",
    )
    promotions = relationship(
        "PromotionsVariants",
        backref="variants",
        cascade="all, delete-orphan",
    )
