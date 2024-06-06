from sqlalchemy import Column, Numeric
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class ClothingSizes(Base):
    __tablename__ = "clothing_sizes"

    back_length = Column(Numeric, nullable=True)
    sleeve_length = Column(Numeric, nullable=True)
    pants_length = Column(Numeric, nullable=True)
    skirt_length = Column(Numeric, nullable=True)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="clothing_sizes"
    )
