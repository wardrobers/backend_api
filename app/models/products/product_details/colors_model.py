from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Colors(Base):
    __tablename__ = "colors"

    name = Column(String)

    # Relationships
    variant = relationship("Variants", backref="colors")
