import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Get database credentials from the DBCRED environment variable
db_credentials = json.loads(os.environ["DBCRED"])
print(db_credentials)
print()

# Construct the database connection string
db_uri = (
    f"postgresql+pg8000://{db_credentials['user']}:{db_credentials['password']}"
    f"@/{db_credentials['database']}?host=/cloudsql/{db_credentials['project']}:"
    f"{db_credentials['region']}:{db_credentials['instance']}" 
)
print(db_uri)
print()
# Create a SQLAlchemy engine
db_engine = create_engine(db_uri)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
