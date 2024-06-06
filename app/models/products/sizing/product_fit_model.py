from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.repositories.common import Base, BaseMixin


class ProductFit(Base, BaseMixin):
    __tablename__ = "product_fit"

    type = Column(String, nullable=False)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="product_fit"
    )
