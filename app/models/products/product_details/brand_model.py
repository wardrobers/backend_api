from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.repositories.common import Base, BaseMixin


class Brand(Base, BaseMixin):
    __tablename__ = "brands"

    name = Column(String, nullable=False)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="brands"
    )
