from enum import Enum, auto
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, between
from pydantic import UUID4

from app.models.products import Product, Category, Size, Brand, Material, Color


class FilterKeys(Enum):
    category_id = auto()
    size_id = auto()
    brand_id = auto()
    material_id = auto()
    color_id = auto()
    price_range = auto()
    available_dates = auto()


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: dict) -> Product:
        new_product = Product(**product_data.dict())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_product(self, uuid: UUID4) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == uuid).first()

    def list_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def update_product(self, uuid: UUID4, product_data: dict) -> Optional[Product]:
        product = self.get_product(uuid)
        if product:
            update_data = product_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)
            self.db.commit()
            return product
        return None

    def delete_product(self, uuid: UUID4):
        product = self.get_product(uuid)
        if product:
            self.db.delete(product)
            self.db.commit()

    def add_category_to_product(self, product_id: UUID4, category_id: UUID4):
        product = self.get_product(product_id)
        category = (
            self.db.query(Category).filter(Category.id == category_id).first()
        )
        if product and category:
            product.categories.append(category)
            self.db.commit()

    def remove_category_from_product(self, product_id: UUID4, category_id: UUID4):
        product = self.get_product(product_id)
        category = (
            self.db.query(Category).filter(Category.id == category_id).first()
        )
        if product and category and category in product.categories:
            product.categories.remove(category)
            self.db.commit()

    def add_material_to_product(self, product_id: UUID4, material_id: UUID4):
        product = self.get_product(product_id)
        material = (
            self.db.query(Material).filter(Material.id == material_id).first()
        )
        if product and material:
            product.materials.append(material)
            self.db.commit()

    def remove_material_from_product(self, product_id: UUID4, material_id: UUID4):
        product = self.get_product(product_id)
        material = (
            self.db.query(Material).filter(Material.id == material_id).first()
        )
        if product and material and material in product.materials:
            product.materials.remove(material)
            self.db.commit()

    def set_color_for_product(self, product_id: UUID4, color_id: UUID4):
        product = self.get_product(product_id)
        color = self.db.query(Color).filter(Color.id == color_id).first()
        if product and color:
            product.color = color
            self.db.commit()

    def remove_color_from_product(self, product_id: UUID4):
        product = self.get_product(product_id)
        if product and product.color:
            product.color = None
            self.db.commit()

    # Methods for handling the product-price relationship
    def add_price_to_product(self, product_id: UUID4, price_data: PriceCreate):
        product = self.get_product(product_id)
        if product:
            new_price = Price(**price_data.dict())
            product.prices.append(new_price)
            self.db.commit()

    def remove_price_from_product(self, product_id: UUID4, price_id: UUID4):
        price = (
            self.db.query(Price)
            .filter(Price.id == price_id, Price.product_id == product_id)
            .first()
        )
        if price:
            self.db.delete(price)
            self.db.commit()

    # Methods for handling the product-brand relationship
    def set_brand_for_product(self, product_id: UUID4, brand_id: UUID4):
        product = self.get_product(product_id)
        brand = self.db.query(Brand).filter(Brand.id == brand_id).first()
        if product and brand:
            product.brand = brand
            self.db.commit()

    def remove_brand_from_product(self, product_id: UUID4):
        product = self.get_product(product_id)
        if product and product.brand:
            product.brand = None
            self.db.commit()

    # Methods for handling the product-size relationship
    def set_size_for_product(self, product_id: UUID4, size_id: UUID4):
        product = self.get_product(product_id)
        size = self.db.query(Size).filter(Size.id == size_id).first()
        if product and size:
            product.size = size
            self.db.commit()

    def remove_size_from_product(self, product_id: UUID4):
        product = self.get_product(product_id)
        if product and product.size:
            product.size = None
            self.db.commit()
