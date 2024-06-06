from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.repositories.common import Base, BaseMixin


class AccessoriesSize(Base, BaseMixin):
    __tablename__ = "accessories_size"

    name = Column(String)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="accessories_size"
    )
