from typing import Optional
from pydantic import UUID4
from sqlalchemy.orm import Session
from ...models.product.color_model import Color
from ...schemas.product.color_schema import ColorCreate, ColorUpdate


class ColorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_color_by_uuid(self, uuid: UUID4) -> Optional[Color]:
        return self.db.query(Color).filter(Color.uuid == uuid).first()

    def create_color(self, color_data: ColorCreate) -> Color:
        new_color = Color(**color_data.dict())
        self.db.add(new_color)
        self.db.commit()
        self.db.refresh(new_color)
        return new_color

    def update_color(self, uuid: UUID4, color_data: ColorUpdate) -> Optional[Color]:
        color = self.get_color_by_uuid(uuid)
        if color:
            for key, value in color_data.dict(exclude_unset=True).items():
                setattr(color, key, value)
            self.db.commit()
            return color
        return None

    def delete_color(self, uuid: UUID4):
        color = self.get_color_by_uuid(uuid)
        if color:
            self.db.delete(color)
            self.db.commit()
