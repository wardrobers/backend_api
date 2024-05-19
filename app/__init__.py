from fastapi import APIRouter

from .routers.product import product_router
from .routers.order import order_router

from app.models import (
    products,
    subscriptions,
    common,
    promotions,
    users,
    orders,
    pricing,
)
from app.database import db_engine, get_db, SessionLocal
from app.routers import user