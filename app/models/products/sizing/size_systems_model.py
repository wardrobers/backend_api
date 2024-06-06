from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.repositories.common import Base, BaseMixin


class SizeSystems(Base, BaseMixin):
    __tablename__ = "size_systems"

    name = Column(String, nullable=False)
    description = Column(Text)

    # Relationships
    sizings = relationship(
        "app.models.products.sizing.sizing_model.Sizing", back_populates="size_system"
    )
