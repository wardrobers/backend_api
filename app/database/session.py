import json
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ..dependencies import get_db_credentials


# Retrieve the database credentials
credentials = get_db_credentials("db-credentials", "477367316624")

# Initialize the Connector object
connector = Connector()


# Function to get database credentials from Google Secret Manager
def get_db_credentials(
    secret_name: str, project_id: str, version_id: str = "latest"
) -> dict:
    # Create a Secret Manager client
    client = secretmanager_v1.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version_id}"

    # Access the secret version
    response = client.access_secret_version(request={"name": name})

    # Decode the secret payload
    secret_string = response.payload.data.decode("UTF-8")

    # Parse the secret payload into a dictionary
    secret_dict = json.loads(secret_string)

    return secret_dict


# Define a function to create a database connection
def getconn() -> sqlalchemy.engine.base.Connection:
    conn = connector.connect(
        credentials["project"],
        "pg8000",
        user=credentials["user"],
        password=credentials["password"],
        db=credentials["database"],
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
