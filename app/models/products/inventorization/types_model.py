from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class Types(Base):
    __tablename__ = "types"

    name = Column(String, nullable=False)

    # Foreign keys
    category_id = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"))

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products",
        secondary="product_types",
        backref="types",
    )
    product_types = relationship(
        "app.models.products.inventorization.types_model.ProductTypes", backref="types"
    )


class ProductTypes(Base):
    __tablename__ = "product_types"

    # Foreign Keys
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, comment="Товар"
    )
    type_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("types.id"), nullable=False, comment="Тип вещи"
    )


class TypesFromUser(Base):
    __tablename__ = "types_from_user"

    coefficient = Column(String)
    raw = Column(JSON)

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type_id = mapped_column(UUID(as_uuid=True), ForeignKey("types.id"))
