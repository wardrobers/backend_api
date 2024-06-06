from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.base_model import Base


class Specifications(Base):
    __tablename__ = "specifications"

    name = Column(String)
    index = Column(Integer)
    value = Column(String)

    # Foreign keys
    article_id = mapped_column(String, ForeignKey("articles.id"), nullable=False)
