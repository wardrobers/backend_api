from sqlalchemy.orm import Session
from typing import Optional
from ...models.product.clothing_size_model import Size
from ...schemas.product.size_schema import SizeCreate, SizeUpdate
from pydantic import UUID4


class SizeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_size_by_uuid(self, uuid: UUID4) -> Optional[Size]:
        return self.db.query(Size).filter(Size.uuid == uuid).first()

    def create_size(self, size_data: SizeCreate) -> Size:
        new_size = Size(**size_data.dict())
        self.db.add(new_size)
        self.db.commit()
        self.db.refresh(new_size)
        return new_size

    def update_size(self, uuid: UUID4, size_data: SizeUpdate) -> Optional[Size]:
        size = self.get_size_by_uuid(uuid)
        if size:
            for key, value in size_data.dict(exclude_unset=True).items():
                setattr(size, key, value)
            self.db.commit()
            return size
        return None

    def delete_size(self, uuid: UUID4) -> None:
        size = self.get_size_by_uuid(uuid)
        if size:
            self.db.delete(size)
            self.db.commit()

    def list_sizes(self, skip: int = 0, limit: int = 10) -> list[Size]:
        return self.db.query(Size).offset(skip).limit(limit).all()
