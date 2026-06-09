# Course Enrollment API

## Overview

Course Enrollment API is a FastAPI-based service for managing users, courses, and student enrollments. It supports user registration, JWT authentication, admin-only course creation, and course enrollment with capacity checks.

## Features

- Register new users with secure password hashing
- Authenticate users and issue JWT access tokens
- List available courses
- Create courses (admin-only)
- Enroll in courses with capacity and duplicate checks
- Database-backed models using SQLAlchemy
- Alembic migrations for schema management

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (via `psycopg2-binary`)
- JWT authentication with `python-jose`
- Password hashing with `passlib`

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/course_enrollment_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Run database migrations:

```bash
alembic upgrade head
```

5. Start the app:

```bash
uvicorn app.main:app --reload
```

6. Open the API docs locally:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Deployment

The live deployment is available at:

`https://course-enrollment-api-1.onrender.com`

For deployed API docs, visit:

- Swagger UI: `https://course-enrollment-api-1.onrender.com/docs`
- ReDoc: `https://course-enrollment-api-1.onrender.com/redoc`

## Environment Variables

- `DATABASE_URL` - SQLAlchemy database connection string
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (usually `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration minutes

## Authentication

- Register with `POST /auth/register`
- Login with `POST /auth/login`
- Both authentication endpoints are rate-limited to prevent abuse
- Use the returned token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

## API Endpoints

### Auth

#### Register user

- `POST /auth/register`
- Request body:
  - `name`: string
  - `email`: string
  - `password`: string
  - `role`: string (`admin` or `student`)

#### Login

- `POST /auth/login`
- Request body:
  - `email`: string
  - `password`: string
- Response:
  - `access_token`: string
  - `token_type`: `bearer`

### Courses

#### Get all courses

- `GET /courses/`
- Public endpoint returning only active courses
- Supports pagination and filtering
- Query parameters:
  - `page`: integer, default `1`
  - `limit`: integer, default `10`, max `100`
  - `q`: string search term for course title or code
- Response: list of course objects

#### Get course by ID

- `GET /courses/{course_id}`
- Public endpoint returning a course by its ID

#### Create course

- `POST /courses/`
- Requires admin authentication
- Request body:
  - `title`: string
  - `code`: string
  - `capacity`: integer > 0

#### Update course

- `PUT /courses/{course_id}`
- Requires admin authentication
- Request body may include:
  - `title`, `capacity`, `is_active`

#### Delete/deactivate course

- `DELETE /courses/{course_id}`
- Requires admin authentication
- Marks a course as inactive

### Enrollments

#### Enroll in a course

- `POST /enrollments/`
- Requires authenticated student
- Request body:
  - `course_id`: integer

#### Deregister from a course

- `DELETE /enrollments/self/{course_id}`
- Requires authenticated student

#### View all enrollments (admin)

- `GET /enrollments/`
- Requires admin authentication

#### View enrollments for a course (admin)

- `GET /enrollments/course/{course_id}`
- Requires admin authentication

#### Remove a student from a course (admin)

- `DELETE /enrollments/{enrollment_id}`
- Requires admin authentication

## Data Models

### User

- `id`: integer
- `name`: string
- `email`: string
- `hashed_password`: string
- `role`: string
- `is_active`: boolean

### Course

- `id`: integer
- `title`: string
- `code`: string
- `capacity`: integer
- `is_active`: boolean

### Enrollment

- `id`: integer
- `user_id`: integer
- `course_id`: integer
- `created_at`: datetime

## Behavior and Validation

- Users must authenticate with JWT for protected actions
- Authentication endpoints are rate-limited to prevent brute-force abuse
- Course listing supports pagination and text search on title/code

- Only users with `role: admin` can create new courses
- Enrollment checks:
  - course exists
  - course is active
  - user is not already enrolled
  - course capacity is not exceeded

## Notes

- Password hashing uses `bcrypt_sha256` for safe handling of long passwords
- Existing bcrypt hashes are still supported for verification
- The app relies on `.env` values loaded by `pydantic-settings`


## Deployment (Leapcell)

This project will be deployed on Leapcell. Add the public deployment URL below once available:

Deployment URL: <LEAPCELL_DEPLOYMENT_URL>

Before replacing the placeholder with the real URL, ensure the following are configured in your Leapcell deployment:

- Environment variables: `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- Run database migrations during deploy: `alembic upgrade head`
- Use a managed Postgres and a Redis instance for rate limiting in production
- Expose health/readiness endpoints and configure monitoring/logging as needed

Replace `<LEAPCELL_DEPLOYMENT_URL>` with the actual Leapcell app link after deployment.

## Development

- Run database migrations with `alembic upgrade head`
- Start the app with `uvicorn app.main:app --reload`
- Run tests with `pytest`
- Use the provided routers and services as the application structure
- Add models, schemas, and repository methods for new entities
