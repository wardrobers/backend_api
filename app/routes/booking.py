from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models.pydantic import BookingCreate, BookingUpdate, Booking
from ..models.sqlalchemy import BookingModel

router = APIRouter()

# Booking System Endpoints
@router.post("/bookings/", response_model=Booking)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = BookingModel(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.get("/bookings/{booking_id}", response_model=Booking)
def read_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/bookings/{booking_id}")
def update_booking(
    booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)
):
    db_booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    for var, value in vars(booking).items():
        setattr(db_booking, var, value) if value else None
    db.commit()
    db.refresh(db_booking)
    return db_booking
