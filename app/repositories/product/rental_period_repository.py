from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from ...models.product.rental_period_model import RentalPeriod
from ...schemas.product.rental_period_schema import (
    RentalPeriodCreate,
    RentalPeriodUpdate,
)


class RentalPeriodRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_rental_period(
        self, rental_period_data: RentalPeriodCreate
    ) -> RentalPeriod:
        new_rental_period = RentalPeriod(**rental_period_data.dict())
        self.db.add(new_rental_period)
        self.db.commit()
        self.db.refresh(new_rental_period)
        return new_rental_period

    def get_rental_period(self, uuid: UUID) -> Optional[RentalPeriod]:
        return self.db.query(RentalPeriod).filter(RentalPeriod.uuid == uuid).first()

    def list_rental_periods(
        self, skip: int = 0, limit: int = 100
    ) -> list[RentalPeriod]:
        return self.db.query(RentalPeriod).offset(skip).limit(limit).all()

    def update_rental_period(
        self, uuid: UUID, rental_period_data: RentalPeriodUpdate
    ) -> Optional[RentalPeriod]:
        rental_period = self.get_rental_period(uuid)
        if rental_period:
            update_data = rental_period_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(rental_period, key, value)
            self.db.commit()
            self.db.refresh(rental_period)
            return rental_period
        return None

    def delete_rental_period(self, uuid: UUID) -> None:
        rental_period = self.get_rental_period(uuid)
        if rental_period:
            self.db.delete(rental_period)
            self.db.commit()
