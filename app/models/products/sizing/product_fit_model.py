from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class ProductFit(Base):
    __tablename__ = "product_fit"

    type = Column(String, nullable=False)

    # Relationships
    product = relationship(
        "Products", backref="product_fit"
    )
