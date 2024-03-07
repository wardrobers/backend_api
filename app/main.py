from fastapi import FastAPI
from .database.session import SessionLocal, db_engine
from .models.basemixin import Base  # Adjust path as necessary
from app import (
    include_api_routers,
)  # Adjust import based on your __init__.py adjustments


def create_tables():
    Base.metadata.create_all(bind=db_engine)


app = FastAPI(title="Wardrobers API", version="2.0")


@app.on_event("startup")
async def startup_event():
    create_tables()


@app.get("/", tags=["Root"])
async def root():
    return {"Welcome to the Wardrobers API!"}


# Including routers
from app.routers import (
    auth_router,
    user_router,
    product_router,
    order_router,
)  # Adjust path as necessary

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(product_router.router, prefix="/products", tags=["Products"])
app.include_router(order_router.router, prefix="/orders", tags=["Orders"])
