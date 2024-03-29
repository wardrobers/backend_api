import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes


# Get database credentials from the DBCRED environment variable
db_credentials = json.loads(os.environ["DBCRED"])

# Configure connector
connector = Connector()  

def getconn() -> sqlalchemy.engine.base.Connection:
    conn = connector.connect(
        db_credentials['project'] + ':' + db_credentials['region'] + ':' + db_credentials['instance'],
        "pg8000",
        user=db_credentials['user'],
        password=db_credentials['password'],
        db=db_credentials['database'],
        ip_type=IPTypes.PUBLIC  # Use PRIVATE if connecting via private IP
    )
    return conn

# Create a SQLAlchemy engine with Cloud SQL Connector
db_engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
