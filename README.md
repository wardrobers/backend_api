# Wardrobers API Repository

## Overview
The Wardrobers API is a robust backend solution for a clothing rental service. It provides comprehensive endpoints for user authentication, clothing management, booking handling, and user reviews. Built with FastAPI, it offers high performance and easy scalability.

## Repository Structure
```
api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main application entry point
│   ├── dependencies.py  # Common dependencies for routes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py  # Database connection and session handling
│   │   ├── sqlalchemy.py  # SQLAlchemy ORM models
│   │   └── pydantic.py  # Pydantic models for data validation
│   └── routes/
│       ├── __init__.py
│       ├── auth.py      # Authentication-related routes
│       ├── user.py      # User management routes
│       ├── clothes.py   # Clothing item routes
│       ├── booking.py   # Booking handling routes
│       └── review.py    # Review and rating routes
└── requirements.txt     # Project dependencies
```

## Setup and Installation

### Prerequisites
- Python 3.10 or higher
- Virtual environment (optional but recommended)

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/wardrobers-api.git
   cd wardrobers-api
   ```

2. **Set Up a Virtual Environment (Optional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Set up necessary environment variables such as `DATABASE_URL` and `JWT_SECRET`. This can be done in a `.env` file or exported directly into your environment.

5. **Run the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication
- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Login for existing users.

### User Management
- **GET /user/{user_id}**: Retrieve user details.
- **PUT /user/{user_id}**: Update user information.

### Clothes Management
- **POST /clothes/**: Add a new clothing item.
- **GET /clothes/**: List all clothing items with optional pagination and sorting.
- **GET /clothes/{clothes_id}**: Retrieve a specific clothing item.
- **PUT /clothes/{clothes_id}**: Update a clothing item.
- **DELETE /clothes/{clothes_id}**: Delete a clothing item.
- **GET /search/clothes/**: Search for clothing items with advanced filters.

### Booking Management
- **POST /booking/**: Create a new booking.
- **GET /booking/{booking_id}**: Retrieve booking details.
- **PUT /booking/{booking_id}**: Update booking information.

### Review Management
- **POST /review/**: Submit a review for a clothing item.
- **PUT /review/{review_id}**: Update a review.

## Running Tests
To run tests, ensure you have a testing environment set up and use a testing framework compatible with FastAPI, such as pytest.

## Connecting to a Database
Ensure your `DATABASE_URL` is set up correctly in your environment. The application uses SQLAlchemy for ORM, which supports multiple databases.

## Security
JWT is used for user authentication. Ensure `JWT_SECRET` is set to a secure, random value in your environment.

## Contributing
Contributions are welcome! Please read our contributing guidelines (if available) for details on how to submit pull requests.