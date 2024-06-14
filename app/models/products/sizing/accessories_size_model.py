from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class AccessoriesSize(Base):
    __tablename__ = "accessories_size"

    name = Column(String)

    # Relationships
    product = relationship(
        "Products", backref="accessories_size"
    )
