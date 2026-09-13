# FastApi-Jwt-Api

A secure RESTful API built with FastAPI featuring JWT authentication, bcrypt password hashing, SQLite database, Pydantic validation, and protected CRUD operations.

## Features

- User registration and login
- JWT Bearer authentication
- Bcrypt password hashing
- Protected user profile
- Product CRUD operations
- SQLite database with SQLAlchemy
- Pydantic request validation
- Swagger/OpenAPI documentation
- Secure environment variables using `.env`

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- Passlib / Bcrypt
- Uvicorn

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/register` | Register a new user | No |
| POST | `/login` | Login and get JWT token | No |
| GET | `/profile` | Get current user profile | Yes |
| POST | `/products` | Create a product | Yes |
| GET | `/products` | Get all products | Yes |
| GET | `/products/{product_id}` | Get one product | Yes |
| PUT | `/products/{product_id}` | Update a product | Yes |
| DELETE | `/products/{product_id}` | Delete a product | Yes |


## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Naina-Shah/FastApi-Jwt-Api.git
cd FastApi-Jwt-Api
## Environment
python -m venv .venv
.venv\Scripts\Activate.ps1

pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv email-validator
## Run
uvicorn main:app --reload

## Open Swagger
http://127.0.0.1:8000/docs

## Authentication

The API uses JWT Bearer authentication for protected endpoints.

1. Register a user using `/register`.
2. Login using `/login` to receive an access token.
3. Open Swagger `/docs`.
4. Click **Authorize**.
5. Enter the JWT token.
6. Access the protected endpoints.

Protected endpoints require a valid JWT token.

## Project Structure

```text
FastApi-Jwt-Api/
├── data/
│   └── app.db
├── main.py
├── database.py
├── model.py
├── schemas.py
├── auth.py
├── .env
├── .gitignore
└── README.md

## API Documentation

Interactive API documentation is available through Swagger UI:

`http://127.0.0.1:8000/docs`

FastAPI also provides the OpenAPI specification at:

`http://127.0.0.1:8000/openapi.json`