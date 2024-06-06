from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.repositories.common import Base, BaseMixin


class ProductPhotos(Base, BaseMixin):
    __tablename__ = "product_photos"

    index = Column(Integer, default=1)
    showcase = Column(Boolean, default=False)

    # Foreign Keys
    product_id = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
