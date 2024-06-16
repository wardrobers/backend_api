from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Brands(Base):
    __tablename__ = "brands"

    name = Column(String, nullable=False)

    # Relationships
    product = relationship("Products", backref="brands")
