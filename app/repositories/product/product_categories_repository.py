from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4, UUID
from ...models.product.product_categories_model import ProductCategory, product_categories
from ...models.product.category_model import Category
import datetime


class ProductCategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product_categories(self, product_uuid: UUID) -> list[Category]:
        return (
            self.db.query(Category)
            .join(product_categories, Category.uuid == product_categories.c.category_uuid)
            .filter(product_categories.c.product_uuid == product_uuid)
            .all()
        )

    def add_category_to_product(
        self, product_uuid: UUID, category_uuid: UUID
    ) -> ProductCategory:
        product_category = ProductCategory(
            uuid=str(uuid4()),
            product_uuid=product_uuid,
            category_uuid=category_uuid,
            created_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.db.add(product_category)
        self.db.commit()
        self.db.refresh(product_category)
        return product_category

    def remove_category_from_product(
        self, product_uuid: UUID, category_uuid: UUID
    ) -> None:
        product_category = (
            self.db.query(ProductCategory)
            .filter_by(product_uuid=product_uuid, category_uuid=category_uuid)
            .first()
        )
        if product_category:
            self.db.delete(product_category)
            self.db.commit()

    def list_all_product_category_relationships(self) -> list[ProductCategory]:
        return self.db.query(ProductCategory).all()

    def get_single_product_category(self, uuid: UUID) -> Optional[ProductCategory]:
        return self.db.query(ProductCategory).filter_by(uuid=uuid).first()

    def update_product_category(
        self, uuid: UUID, update_fields: dict
    ) -> Optional[ProductCategory]:
        product_category = self.db.query(ProductCategory).filter_by(uuid=uuid).first()
        if product_category:
            for key, value in update_fields.items():
                setattr(product_category, key, value)
            self.db.commit()
            self.db.refresh(product_category)
            return product_category
        return None

    def delete_product_category(self, uuid: UUID) -> None:
        product_category = self.get_single_product_category(uuid)
        if product_category:
            self.db.delete(product_category)
            self.db.commit()
