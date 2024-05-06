from typing import Optional
from pydantic import UUID4
from sqlalchemy.orm import Session
from ...models.products.pricing_table_model import Price
from ...schemas.product.price_schema import PriceCreate, PriceUpdate


class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_price_by_uuid(self, uuid: UUID4) -> Optional[Price]:
        return self.db.query(Price).filter(Price.uuid == uuid).first()

    def create_price(self, price_data: PriceCreate) -> Price:
        new_price = Price(**price_data.dict())
        self.db.add(new_price)
        self.db.commit()
        self.db.refresh(new_price)
        return new_price

    def update_price(self, uuid: UUID4, price_data: PriceUpdate) -> Optional[Price]:
        price = self.get_price_by_uuid(uuid)
        if price:
            for key, value in price_data.dict(exclude_unset=True).items():
                setattr(price, key, value)
            self.db.commit()
            return price
        return None

    def delete_price(self, uuid: UUID4):
        price = self.get_price_by_uuid(uuid)
        if price:
            self.db.delete(price)
            self.db.commit()

    def get_prices_for_rental_period(self, rental_period_uuid: UUID4) -> list[Price]:
        return (
            self.db.query(Price)
            .filter(Price.time_period_uuid == rental_period_uuid)
            .all()
        )
