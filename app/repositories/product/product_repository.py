from typing import Optional
from pydantic import UUID4
from sqlalchemy.orm import Session
from .models import Product, Category, Material, Color, Size
from .schemas import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: ProductCreate) -> Product:
        new_product = Product(**product_data.dict())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_product(self, uuid: UUID4) -> Optional[Product]:
        return self.db.query(Product).filter(Product.uuid == uuid).first()

    def list_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def update_product(self, uuid: UUID4, product_data: ProductUpdate) -> Optional[Product]:
        product = self.get_product(uuid)
        if product:
            update_data = product_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)
            self.db.commit()
            return product
        return None

    def delete_product(self, uuid: str):
        product = self.get_product(uuid)
        if product:
            self.db.delete(product)
            self.db.commit()

    def add_category_to_product(self, product_uuid: UUID4, category_uuid: UUID4):
        product = self.get_product(product_uuid)
        category = self.db.query(Category).filter(Category.uuid == category_uuid).first()
        if product and category:
            product.categories.append(category)
            self.db.commit()

    def remove_category_from_product(self, product_uuid: UUID4, category_uuid: UUID4):
        product = self.get_product(product_uuid)
        category = self.db.query(Category).filter(Category.uuid == category_uuid).first()
        if product and category and category in product.categories:
            product.categories.remove(category)
            self.db.commit()

    def add_material_to_product(self, product_uuid: UUID4, material_uuid: UUID4):
        product = self.get_product(product_uuid)
        material = self.db.query(Material).filter(Material.uuid == material_uuid).first()
        if product and material:
            product.materials.append(material)
            self.db.commit()

    def remove_material_from_product(self, product_uuid: UUID4, material_uuid: UUID4):
        product = self.get_product(product_uuid)
        material = self.db.query(Material).filter(Material.uuid == material_uuid).first()
        if product and material and material in product.materials:
            product.materials.remove(material)
            self.db.commit()

    def set_color_for_product(self, product_uuid: UUID4, color_uuid: UUID4):
        product = self.get_product(product_uuid)
        color = self.db.query(Color).filter(Color.uuid == color_uuid).first()
        if product and color:
            product.color = color
            self.db.commit()

    def remove_color_from_product(self, product_uuid: UUID4):
        product = self.get_product(product_uuid)
        if product and product.color:
            product.color = None
            self.db.commit()

    # Methods for handling the product-price relationship
    def add_price_to_product(self, product_uuid: UUID4, price_data: PriceCreate):
        product = self.get_product(product_uuid)
        if product:
            new_price = Price(**price_data.dict())
            product.prices.append(new_price)
            self.db.commit()

    def remove_price_from_product(self, product_uuid: UUID4, price_uuid: UUID4):
        price = self.db.query(Price).filter(Price.uuid == price_uuid, Price.product_uuid == product_uuid).first()
        if price:
            self.db.delete(price)
            self.db.commit()

    # Methods for handling the product-brand relationship
    def set_brand_for_product(self, product_uuid: UUID4, brand_uuid: UUID4):
        product = self.get_product(product_uuid)
        brand = self.db.query(Brand).filter(Brand.uuid == brand_uuid).first()
        if product and brand:
            product.brand = brand
            self.db.commit()

    # Methods for handling the product-size relationship
    def set_size_for_product(self, product_uuid: UUID4, size_uuid: UUID4):
        product = self.get_product(product_uuid)
        size = self.db.query(Size).filter(Size.uuid == size_uuid).first()
        if product and size:
            product.size = size
            self.db.commit()

    def remove_size_from_product(self, product_uuid: UUID4):
        product = self.get_product(product_uuid)
        if product and product.size:
            product.size = None
            self.db.commit()
