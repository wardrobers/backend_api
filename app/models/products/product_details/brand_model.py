from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models import Base


class Brand(Base):
    __tablename__ = "brands"

    name = Column(String, nullable=False)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="brands"
    )
