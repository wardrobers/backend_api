# Wardrobers Backend API Repository Overview

The Wardrobers Backend API is a FastAPI-based service designed to facilitate fashion item rental transactions. Our repository's architecture is strategically modularized, promoting separation of concerns, scalability, and ease of maintenance.

## Repository Structure and Logic

### `app/`: The Application Core

- `__init__.py`: This file orchestrates the inclusion of routers into the main application, effectively assembling our API's endpoint structure.
- `main.py`: Serving as the application's nerve center, this file initializes the FastAPI instance, database tables, and event handlers for startup and shutdown events.

### `database/`: Database Interactions

- Manages database sessions and connections using SQLAlchemy, allowing for a seamless interface with the backend SQL database.
- `session.py`: Defines the session maker and connection handler, utilizing Google Cloud SQL for reliable database operations.

### `models/`: Data Modeling

- Contains SQLAlchemy ORM models, each representing a table in the database.
- These models are crucial for mirroring the database schema in Python code, providing a robust groundwork for database interactions.

### `repositories/`: Business Logic Encapsulation

- Each repository file corresponds to a model, with classes containing methods for creating, retrieving, updating, and deleting records.
- The use of repositories abstracts the complexity of direct database manipulation, providing a clean interface for the routers to interact with the database.

### `routers/`: API Endpoints Definition

- Comprises multiple modules, each defining a set of related endpoints and their logic.
- Routers handle incoming HTTP requests, interact with the appropriate repositories, and return the correct HTTP responses.

### `schemas/`: Data Validation and Serialization

- Utilizes Pydantic models to enforce type checking and validation of request and response data.
- Schemas ensure that data transferred between the client and server adheres to the defined structure, fostering data integrity.

### `authentication/`: Security Measures

- Implements JWT-based authentication, providing secure access to the API.
- The `security.py` file manages password hashing and token generation, safeguarding user credentials and sessions.

## Repository Flow

When the application starts:

1. `main.py` invokes the database connection setup.
2. Tables are generated based on `models/`.
3. Routers are imported and included in the API, making the endpoints active.
4. The API is now ready to handle requests, with `routers/` directing traffic to the correct repository for data handling.

Upon receiving a request:

1. The request is validated against schemas in `schemas/`.
2. The router processes the request, delegating operations to the corresponding repository.
3. Repositories perform CRUD operations using models as blueprints for the database.
4. Responses are serialized as defined in `schemas/` and sent back to the client.

## Visual Repository Scheme

```plaintext
/backend_api
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database/
│   │   └── session.py
│   ├── models/
│   │   └── *.py
│   ├── repositories/
│   │   └── *.py
│   ├── routers/
│   │   └── *.py
│   ├── schemas/
│   │   └── *.py
│   └── authentication/
│       └── security.py
├── Dockerfile
└── requirements.txt
```

## Local Development Guide for Wardrobers Backend API

This guide outlines the steps necessary to set up a local development environment for Wardrobers Backend API. By following these instructions, developers can work in an isolated environment, ensuring consistency across various setups and streamlined integration with the necessary Google Cloud Platform (GCP) services.

### Prerequisites
Before starting, ensure you have the following installed:
- [Python 3.11](https://www.python.org/downloads/)
- [Conda](https://docs.conda.io/en/latest/)
- [Google Cloud SDK](https://cloud.google.com/sdk)
- Docker (optional, for containerized environments)

### Environment Setup

#### 1. Clone the Repository
Begin by cloning the Wardrobers backend repository and navigate to the `backend_API` directory.

```bash
git clone https://github.com/wardrobers/backend_api.git
cd backend_api
```

#### 2. Create a Conda Environment
Create an isolated Conda environment specifically for Wardrobers development.

```bash
conda create --name wardrobers_env python=3.11
```

#### 3. Activate the Conda Environment
Switch to the newly created Conda environment.

```bash
conda activate wardrobers_env
```

### 4. Install Dependencies
Install the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

#### 5. Google Cloud Authentication
Authenticate with GCP using the provided service account. For sign in use your Wardrobers email `<your-email>@wdbrs.co`.

```bash
gcloud auth application-default login --impersonate-service-account=wardrobers-dev@feisty-enigma-409319.iam.gserviceaccount.com
```

### Running the Application

#### Option 1: Directly with Uvicorn
Run the FastAPI application using Uvicorn, specifying the host and port.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

#### Option 2: With Docker
If you prefer to use Docker, update the Dockerfile to include GCP authentication as demonstrated above.

Build the Docker image:

```bash
docker build -t wardrobers-backend .
```

Run the Docker container:

```bash
docker run -p 8080:8080 wardrobers-backend
```
