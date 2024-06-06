from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models import Base


class TypesOfOperations(Base):
    __tablename__ = "types_of_operations"

    name = Column(String, nullable=True, default=None)

    # Relationships
    articles = relationship(
        "app.models.products.core.articles_model.Articles",
        backref="types_of_operations",
    )
