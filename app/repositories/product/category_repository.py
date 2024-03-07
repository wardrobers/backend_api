from sqlalchemy.orm import Session
from ...models.product.category_model import Category
from ...schemas.product.category_schema import CategoryCreate, CategoryUpdate
from uuid import UUID


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category_data: CategoryCreate) -> Category:
        new_category = Category(**category_data.dict())
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

    def get_category_by_uuid(self, uuid: UUID) -> Category:
        return self.db.query(Category).filter(Category.uuid == uuid).first()

    def update_category(self, uuid: UUID, update_data: CategoryUpdate) -> Category:
        category = self.get_category_by_uuid(uuid)
        if category:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(category, key, value)
            self.db.commit()
            self.db.refresh(category)
            return category
        return None

    def delete_category(self, uuid: UUID) -> None:
        category = self.get_category_by_uuid(uuid)
        if category:
            self.db.delete(category)
            self.db.commit()

    def list_categories(self, skip: int = 0, limit: int = 10) -> list[Category]:
        return self.db.query(Category).offset(skip).limit(limit).all()
