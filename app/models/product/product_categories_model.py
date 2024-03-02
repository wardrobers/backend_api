from sqlalchemy import Column, DateTime, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Many-to-Many relationship helper tables
product_categories = Table(
    "product_categories",
    Base.metadata,
    Column(
        "product_uuid",
        UUID(as_uuid=True),
        ForeignKey("products.uuid"),
        primary_key=True,
    ),
    Column(
        "category_uuid",
        UUID(as_uuid=True),
        ForeignKey("categories.uuid"),
        primary_key=True,
    ),
)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    product_catalog_uuid = Column("product_catalog_uuid", String, nullable=False)
    category_uuid = Column("category_uuid", String, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    deleted_at = Column("deleted_at", DateTime)
