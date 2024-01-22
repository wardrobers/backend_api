from fastapi import FastAPI

from app.routes import booking, clothes, review, users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["UserAuthentication"])
app.include_router(clothes.router, prefix="/clothes", tags=["Clothes"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])
app.include_router(review.router, prefix="/review", tags=["Review"])
