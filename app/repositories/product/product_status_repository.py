from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from ...models.products.product_details.product_status_model import ProductStatus
from ...schemas.product.product_status_schema import (
    ProductStatusCreate,
    ProductStatusUpdate,
)


class ProductStatusRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product_status(self, status_data: ProductStatusCreate) -> ProductStatus:
        new_status = ProductStatus(**status_data.dict())
        self.db.add(new_status)
        self.db.commit()
        self.db.refresh(new_status)
        return new_status

    def get_product_status(self, uuid: UUID) -> Optional[ProductStatus]:
        return self.db.query(ProductStatus).filter(ProductStatus.id == uuid).first()

    def list_product_statuses(
        self, skip: int = 0, limit: int = 100
    ) -> list[ProductStatus]:
        return self.db.query(ProductStatus).offset(skip).limit(limit).all()

    def update_product_status(
        self, uuid: UUID, status_data: ProductStatusUpdate
    ) -> Optional[ProductStatus]:
        status = self.get_product_status(uuid)
        if status:
            update_data = status_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(status, key, value)
            self.db.commit()
            self.db.refresh(status)
            return status
        return None

    def delete_product_status(self, uuid: UUID) -> None:
        status = self.get_product_status(uuid)
        if status:
            self.db.delete(status)
            self.db.commit()
