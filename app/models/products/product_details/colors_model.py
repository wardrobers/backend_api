from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.repositories.common import Base, BaseMixin


class Colors(Base, BaseMixin):
    __tablename__ = "colors"

    name = Column(String)

    # Relationships
    variant = relationship(
        "app.models.products.core.variants_model.Variants", backref="colors"
    )
