from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4

from ..dependencies import get_db
from ..repositories.order_repository import OrderRepository
from ..schemas.order_schema import OrderCreate, OrderRead, OrderUpdate

router = APIRouter()

@router.post("/orders/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order_create: OrderCreate, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    new_order = order_repository.create_order(order_create)
    if not new_order:
        raise HTTPException(status_code=400, detail="Could not create the order")
    return new_order

@router.get("/orders/{order_uuid}", response_model=OrderRead)
def get_order(order_uuid: UUID4, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    order = order_repository.get_order_by_uuid(order_uuid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/users/{user_uuid}/orders/", response_model=list[OrderRead])
def list_orders_for_user(user_uuid: UUID4, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    orders = order_repository.list_orders_by_user_uuid(user_uuid)
    return orders

@router.put("/orders/{order_uuid}", response_model=OrderRead)
def update_order(order_uuid: UUID4, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    updated_order = order_repository.update_order(order_uuid, order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found or could not be updated")
    return updated_order

@router.put("/orders/{order_uuid}/status", response_model=OrderRead)
def update_order_status(order_uuid: UUID4, order_status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    order_status_repository = OrderStatusRepository(db)  # Use this repository to handle status updates
    updated_order_status = order_status_repository.update_order_status(order_uuid, order_status_update)
    if not updated_order_status:
        raise HTTPException(status_code=404, detail="Order status not found or could not be updated")
    return updated_order_status

@router.delete("/orders/{order_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_uuid: UUID4, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    success = order_repository.delete_order(order_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found or could not be deleted")
    return {"detail": "Order deleted successfully"}
