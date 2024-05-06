from sqlalchemy.orm import Session
from typing import Optional
from ...models.orders.core.order_model import Order
from ...schemas.order.order_schema import OrderCreate, OrderRead, OrderUpdate
from pydantic import UUID4


class OrderRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_order(self, order_data: OrderCreate) -> OrderRead:
        new_order = Order(
            # user_uuid=order_data.user_uuid,
            # product_uuid=order_data.product_uuid,
            start=order_data.start,
            end=order_data.end,
            price=order_data.price,
        )
        self.db_session.add(new_order)
        self.db_session.commit()
        self.db_session.refresh(new_order)
        return new_order

    def get_order_by_uuid(self, uuid: UUID4) -> Optional[OrderRead]:
        return self.db_session.query(Order).filter(Order.uuid == uuid).first()

    def list_orders_by_user_uuid(
        self, user_uuid: UUID4, skip: int = 0, limit: int = 100
    ) -> list[OrderRead]:
        return (
            self.db_session.query(Order)
            .filter(Order.user_uuid == user_uuid)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_order(self, uuid: UUID4, order_data: OrderUpdate) -> Optional[OrderRead]:
        order = self.db_session.query(Order).filter(Order.uuid == uuid).first()
        if order:
            order.start = order_data.start if order_data.start else order.start
            order.end = order_data.end if order_data.end else order.end
            order.price = order_data.price if order_data.price else order.price
            self.db_session.commit()
            return order
        return None

    def delete_order(self, uuid: str):
        order = self.db_session.query(Order).filter(Order.uuid == uuid).first()
        if order:
            self.db_session.delete(order)
            self.db_session.commit()
