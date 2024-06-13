import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

ENV = os.getenv("ENV", default="development")
DATABASE_URL = os.getenv("DATABASE_URL")


# Create the synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=ENV != "production")

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)


def get_db():
    """
    Provides a database session within a request context. The session is closed
    automatically after the request.
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()
