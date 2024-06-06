from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models import Base


class Colors(Base):
    __tablename__ = "colors"

    name = Column(String)

    # Relationships
    variant = relationship(
        "app.models.products.core.variants_model.Variants", backref="colors"
    )
