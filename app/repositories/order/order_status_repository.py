from sqlalchemy.orm import Session
from typing import Optional
from ...models.orders.core.order_status_model import (
    OrderStatus,
)  # Assuming your model file is named models.py
from ...schemas.order.order_status_schema import (
    OrderStatusCreate,
    OrderStatusRead,
    OrderStatusUpdate,
)
from pydantic import UUID4


class OrderStatusRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_order_status(
        self, order_status_data: OrderStatusCreate
    ) -> OrderStatusRead:
        new_order_status = OrderStatus(**order_status_data.dict())
        self.db_session.add(new_order_status)
        self.db_session.commit()
        self.db_session.refresh(new_order_status)
        return new_order_status

    def get_order_status_by_uuid(self, uuid: UUID4) -> Optional[OrderStatusRead]:
        return (
            self.db_session.query(OrderStatus).filter(OrderStatus.uuid == uuid).first()
        )

    def list_order_statuses(
        self, skip: int = 0, limit: int = 100
    ) -> list[OrderStatusRead]:
        return self.db_session.query(OrderStatus).offset(skip).limit(limit).all()

    def update_order_status(
        self, uuid: UUID4, order_status_data: OrderStatusUpdate
    ) -> Optional[OrderStatusRead]:
        order_status = (
            self.db_session.query(OrderStatus).filter(OrderStatus.uuid == uuid).first()
        )
        if order_status:
            if order_status_data.code is not None:
                order_status.code = order_status_data.code
            if order_status_data.name is not None:
                order_status.name = order_status_data.name
            self.db_session.commit()
            return order_status
        return None

    def delete_order_status(self, uuid: UUID4):
        order_status = (
            self.db_session.query(OrderStatus).filter(OrderStatus.uuid == uuid).first()
        )
        if order_status:
            self.db_session.delete(order_status)
            self.db_session.commit()
