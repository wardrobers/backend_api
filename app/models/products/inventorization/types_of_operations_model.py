from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class TypesOfOperations(Base):
    __tablename__ = "types_of_operations"

    name = Column(String, nullable=True, default=None)

    # Relationships
    articles = relationship(
        "Articles",
        backref="types_of_operations",
    )
