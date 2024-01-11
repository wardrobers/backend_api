from fastapi import FastAPI
from .routes import auth, user, clothes, booking, review

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(clothes.router, prefix="/clothes", tags=["Clothes"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])
app.include_router(review.router, prefix="/review", tags=["Review"])
