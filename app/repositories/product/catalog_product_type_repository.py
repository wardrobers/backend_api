from sqlalchemy.orm import Session
from ...models.products.catalog_product_type_model import CatalogProductType
from uuid import UUID


class CatalogProductTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_catalog_product_type(
        self, product_type_id: UUID, products_catalog_id: UUID
    ) -> CatalogProductType:
        new_catalog_product_type = CatalogProductType(
            product_type_id=product_type_id,
            products_catalog_id=products_catalog_id,
        )
        self.db.add(new_catalog_product_type)
        self.db.commit()
        self.db.refresh(new_catalog_product_type)
        return new_catalog_product_type

    def get_catalog_product_type(self, uuid: UUID) -> CatalogProductType:
        return self.db.query(CatalogProductType).filter_by(uuid=uuid).first()

    def update_catalog_product_type(self, uuid: UUID, **kwargs) -> CatalogProductType:
        catalog_product_type = self.get_catalog_product_type(uuid)
        if catalog_product_type:
            for key, value in kwargs.items():
                setattr(catalog_product_type, key, value)
            self.db.commit()
            self.db.refresh(catalog_product_type)
        return catalog_product_type

    def delete_catalog_product_type(self, uuid: UUID) -> None:
        catalog_product_type = self.get_catalog_product_type(uuid)
        if catalog_product_type:
            self.db.delete(catalog_product_type)
            self.db.commit()

    def list_catalog_product_types(
        self, skip: int = 0, limit: int = 100
    ) -> list[CatalogProductType]:
        return self.db.query(CatalogProductType).offset(skip).limit(limit).all()
