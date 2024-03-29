import os
import json
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from sqlalchemy.orm import sessionmaker


# Initialize the Connector object
connector = Connector()


# Get database credentials from the DBCRED environment variable
db_credentials = json.loads(os.environ["DBCRED"])


# Define a function to create a database connection
def getconn() -> sqlalchemy.engine.base.Connection:
    conn = connector.connect(
        db_credentials["project"],
        "pg8000",
        user=db_credentials["user"],
        password=db_credentials["password"],
        db=db_credentials["database"],
        ip_type=IPTypes.PUBLIC,  # Use PRIVATE for private IP or PUBLIC for public IP
    )
    return conn


# Create a SQLAlchemy engine using the connection created by the Connector
db_engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Create a new sessionmaker using the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
