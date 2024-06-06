from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models import Base


class ProductFit(Base):
    __tablename__ = "product_fit"

    type = Column(String, nullable=False)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="product_fit"
    )
