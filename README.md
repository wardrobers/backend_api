# Wardrobers Backend API

This repository houses the backend API for Wardrobers, a fashion rental platform. The API is built using FastAPI and interacts with a PostgreSQL database via SQLAlchemy. 

## Project Structure and Logic

The project follows a layered architecture to enhance organization, maintainability, and scalability:

### Core Components:

- **`app/`:** Contains the heart of the application logic.
    - **`__init__.py`:** Assembles the application by including routers.
    - **`main.py`:** Initializes FastAPI, sets up database connections, and handles startup/shutdown events.
    - **`database/`:** Manages database interactions.
        - **`session.py`:** Defines database session and connection management using SQLAlchemy, including handling connections to Cloud SQL. 
    - **`models/`:** Houses SQLAlchemy ORM models that represent database tables. Each model maps to a specific database table, defining its structure, relationships, and data types. 
        - **`users/`:** Models related to user management, profiles, authentication, etc.
        - **`products/`:** Models for products, variations, categories, materials, etc.
        - **`orders/`:** Models for orders, order items, shipping details, payment information, etc.
        - **`subscriptions/`:** Models related to user subscriptions.
        - **`promotions/`:** Models for promotions, discounts, and their application logic.
        - **`pricing/`:**  Models defining pricing tiers, rules, and calculations.
        - **`common/`:** Base models and mixins with common functionality used across other models, such as the `BaseMixin` for common CRUD operations.
        - **`authentication/`:** Models and logic for handling user authentication and security. 
    - **`routers/`:** Defines API endpoints and handles HTTP requests. Routers use services to perform business logic.
        - **`users/`:**  Routers for user-related actions (registration, authentication, profile management).
    - **`schemas/`:** Contains Pydantic models for data validation and serialization. These schemas define the structure and data types expected for requests and responses, ensuring data integrity.
    - **`tests/`:** A comprehensive suite of automated tests covering unit tests for models, services, and integration tests for API routes.
        - **`basics/`:**  Fundamental tests for code structure, database connection, schema consistency, etc.
        - **`users/`:**  Tests specifically for the `users/` models and services.
        - **`products/`:** Tests for the `products/` models and services. 
        - **`orders/`:** Tests related to orders, order processing, etc.
        - **`integration/`:** End-to-end tests for API routes and interactions between components.
- **`requirements.txt`:** Lists the Python project dependencies.
- **`Dockerfile`:** Defines instructions for building the Docker image. 

### Introducing Repositories and Services

To further improve code organization and maintainability, the project will be updated to include:

- **`repositories/`:** This folder will contain classes responsible for interacting with the database. Each repository class will be dedicated to a specific model (e.g., `product_repository.py`, `user_repository.py`) and will provide methods for common CRUD operations. 
- **`services/`:** This folder will contain classes that encapsulate the business logic of the application. Services will interact with repositories to perform operations and handle complex workflows. 

This separation allows for cleaner code, better testability, and improved scalability as the project grows. 

## Request Flow

Here's how a typical request will be handled by the application:

1. **Client Request:** The client sends an HTTP request to an API endpoint defined in a router.
2. **Validation:** The router validates the incoming data using the corresponding Pydantic schema from `schemas/`.
3. **Service Invocation:** The router invokes the appropriate service from `services/` to process the request.
4. **Repository Interaction:** The service uses one or more repositories from `repositories/` to interact with the database.
5. **Database Operations:** Repositories execute queries using SQLAlchemy ORM models defined in `models/`.
6. **Business Logic:** The service applies the necessary business logic, data transformations, and error handling.
7. **Response Preparation:** The service returns the result to the router.
8. **Serialization:** The router serializes the response data using Pydantic schemas.
9. **Client Response:**  The router sends the serialized response back to the client.

## Local Development Guide

### Prerequisites

- **Python 3.11:** Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Conda:** (Recommended) For environment management. Download from [https://docs.conda.io/en/latest/](https://docs.conda.io/en/latest/)
- **Docker:** (Optional) For containerized development. Download from [https://www.docker.com/get-started](https://www.docker.com/get-started)
- **Docker Compose:** (Optional) For orchestrating multi-container applications. Download along with Docker.

### Environment Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/wardrobers/backend_api.git
   cd backend_api
   ```

2. **Create a Conda Environment (Recommended):**

   ```bash
   conda create --name wardrobers_env python=3.11
   conda activate wardrobers_env
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the project's root directory and define these variables (replace placeholders with your actual credentials):
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   REDISCRED={"host":"your_redis_host", "port": your_redis_port, "password": "your_redis_password"}
   AUTH_SECRET_KEY={"auth_secret_key":"your_secret_key"}
   ```
- For local development, you can use a local PostgreSQL instance.

### Running the Application

**1. Directly with Uvicorn (without Docker):**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload 
   ```

**2. With Docker Compose:**

   - Create a `docker-compose.yml` file in the root of your project: 
   ```yaml
   version: '3.8'

   services:
     db:
       image: postgres:15
       volumes:
         - postgres_data:/var/lib/postgresql/data
       environment:
         POSTGRES_DB: wardrobers_test
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: password  # Change this for production and use environment variables

     app:
       build: .
       ports:
         - "8080:8080"
       depends_on:
         - db
       environment:
         DATABASE_URL: postgresql://postgres:password@db:5432/wardrobers_test
         ENV: development  # This can be overridden in production

   volumes:
     postgres_data:
   ```
   - Build and start the services:
     ```bash
     docker-compose up -d --build
     ```
   - Access your application at `http://localhost:8080`. 

## Testing

Run the test suite with:

    ```bash
    pytest
    ```

This command executes all the tests in the `tests/` directory, covering unit and integration tests. 