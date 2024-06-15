from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class SizeSystems(Base):
    __tablename__ = "size_systems"

    name = Column(String, nullable=False)
    description = Column(Text)

    # Relationships
    sizings = relationship("Sizing", backref="size_system")
