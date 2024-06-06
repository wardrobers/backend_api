from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class ClaspType(Base):
    __tablename__ = "clasp_types"

    name = Column(String, nullable=True)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="clasp_types"
    )
