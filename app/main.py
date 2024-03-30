from fastapi import FastAPI, HTTPException, Request
from .database.session import db_engine, get_db, SessionLocal
from .models.basemixin import Base  # Adjust path as necessary


def create_tables():
    Base.metadata.create_all(bind=db_engine)


app = FastAPI(title="Wardrobers API", version="2.0")


@app.on_event("startup")
async def startup_event():
    create_tables()

# Middleware for DB session management
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    request.state.db = SessionLocal()
    try:
        # Attach a new session to the request state
        response = await call_next(request)
    except Exception as e:
        # Handle exceptions and potentially roll back transactions here
        request.state.db.rollback()
        raise e
    finally:
        # Always close the session after the request is done
        request.state.db.close()
    return response

@app.get("/", tags=["Root"])
async def root():
    return {"Welcome to the Wardrobers API!"}

@app.get("/healthz", tags=["Test"])
async def liveness_check():
    try:
        # 1. Database Connectivity
        with get_db() as db:
            # Test a simple query to verify the connection
            db.execute("SELECT 1")

        # 2. (Optional) External Dependency Checks
        # If Wardrobers relies on other services (e.g., image storage, third-party APIs)
        # Add checks to make API requests to those external dependencies here

        return {"status": "ok", "dependencies": {"database": "ok"}}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")


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
