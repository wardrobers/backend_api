from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import UUID4
from typing import Optional

from ...database.session import get_db
from ...repositories.order.order_repository import OrderRepository
from ...repositories.order.order_status_repository import OrderStatusRepository
from ...schemas.order.order_schema import OrderCreate, OrderRead, OrderUpdate
from ...schemas.order.order_status_schema import OrderStatusUpdate

router = APIRouter()


@router.post(
    "/", response_model=Optional[OrderRead], status_code=status.HTTP_201_CREATED
)
def create_order(order_create: OrderCreate, request: Request):
    db: Session = request.state.db
    order_repository = OrderRepository(db)
    new_order = order_repository.create_order(order_create)
    if not new_order:
        raise HTTPException(status_code=400, detail="Could not create the order")
    return new_order


@router.get("/get", response_model=OrderRead)
def get_order(order_id: UUID4, request: Request):
    db: Session = request.state.db
    order_repository = OrderRepository(db)
    order = order_repository.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/list_all", response_model=list[OrderRead])
def list_orders_for_user(user_id: UUID4, request: Request):
    db: Session = request.state.db
    order_repository = OrderRepository(db)
    orders = order_repository.list_orders_by_user_id(user_id)
    return orders


@router.put("/update", response_model=OrderRead)
def update_order(order_id: UUID4, order_update: OrderUpdate, request: Request):
    db: Session = request.state.db
    order_repository = OrderRepository(db)
    updated_order = order_repository.update_order(order_id, order_update)
    if not updated_order:
        raise HTTPException(
            status_code=404, detail="Order not found or could not be updated"
        )
    return updated_order


@router.put("/update_status", response_model=OrderRead)
def update_order_status(
    order_id: UUID4, order_status_update: OrderStatusUpdate, request: Request
):
    db: Session = request.state.db
    order_status_repository = OrderStatusRepository(
        db
    )  # Use this repository to handle status updates
    updated_order_status = order_status_repository.update_order_status(
        order_id, order_status_update
    )
    if not updated_order_status:
        raise HTTPException(
            status_code=404, detail="Order status not found or could not be updated"
        )
    return updated_order_status


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID4, request: Request):
    db: Session = request.state.db
    order_repository = OrderRepository(db)
    success = order_repository.delete_order(order_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Order not found or could not be deleted"
        )
    return {"detail": "Order deleted successfully"}
