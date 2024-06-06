from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models import Base


class AccessoriesSize(Base):
    __tablename__ = "accessories_size"

    name = Column(String)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="accessories_size"
    )
