# Leaderboard Backend Application

A simple leaderboard backend API built with FastAPI and PostgreSQL.

## Quick Start

1. **Install dependencies** (if not already done):
   ```bash
   pip install -e .
   ```

2. **Set up PostgreSQL database**:
   
   **Option A: Using Docker (recommended)**
   ```bash
   docker-compose up -d
   ```
   This will start PostgreSQL with the default credentials from `.env`
   
   **Option B: Using existing PostgreSQL**
   ```sql
   CREATE DATABASE leaderboard;
   ```
   Update `.env` file with your database credentials.

3. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```
   Or use the PowerShell script:
   ```powershell
   .\run.ps1
   ```

5. **Test the API**:
   - **Interactive Swagger UI:** http://localhost:8000/docs
   - **ReDoc Documentation:** http://localhost:8000/redoc
   - Or run the test script: `python test_api.py`

## Features

- **List leaderboard** - Get all users sorted by score (highest to lowest)
- **Add users** - Register new users with initial score of 0
- **Update scores** - Modify user scores by name
- **Get version** - Retrieve current API version
- **Interactive API Documentation** - Full Swagger/OpenAPI documentation
- **SQLAlchemy ORM** - Type-safe database operations
- **Alembic Migrations** - Version-controlled database schema
- **PostgreSQL database** - Async connection pooling
- **Environment Configuration** - .env file with environment variable override

## Prerequisites

- Python 3.10 or higher
- PostgreSQL database server

## Installation

1. Install dependencies:
```bash
pip install -e .
```

2. Configure the database:
   - Copy `.env.example` to `.env` (already done)
   - Update the PostgreSQL connection settings in `.env`:
     ```
     POSTGRES_HOST=localhost
     POSTGRES_PORT=5432
     POSTGRES_DB=leaderboard
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=postgres
     ```

3. Create the PostgreSQL database:
```sql
CREATE DATABASE leaderboard;
```

The application will automatically create the required tables on startup.

## Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Interactive API Documentation

The Leaderboard API includes comprehensive **Swagger/OpenAPI documentation**:

### Swagger UI (Recommended)
**URL:** http://localhost:8000/docs

Features:
- 🎯 Interactive interface to test all endpoints
- 📝 Complete request/response schemas
- ✅ Live validation and examples
- 🏷️ Organized by tags (leaderboard, users, system)

### ReDoc
**URL:** http://localhost:8000/redoc

Features:
- 📖 Clean, three-panel documentation
- 🔍 Search functionality
- 📱 Mobile-friendly interface

### OpenAPI Schema
**URL:** http://localhost:8000/openapi.json
- Raw OpenAPI 3.0 JSON schema

> 💡 **See [SWAGGER_DOCS.md](SWAGGER_DOCS.md) for detailed documentation guide**

## API Endpoints

### 1. List Leaderboard
```http
GET /leaderboard
```
Returns all users ordered by score (highest to lowest).

**Response:**
```json
[
  {
    "id": 1,
    "name": "Alice",
    "score": 100,
    "created_at": "2026-02-28T10:00:00",
    "updated_at": "2026-02-28T10:00:00"
  }
]
```

### 2. Add User
```http
POST /user
Content-Type: application/json

{
  "name": "Alice"
}
```
Adds a new user with an initial score of 0.

**Response:**
```json
{
  "message": "User added successfully",
  "data": {
    "id": 1,
    "name": "Alice",
    "score": 0
  }
}
```

### 3. Update Score
```http
PUT /user/score
Content-Type: application/json

{
  "name": "Alice",
  "score": 100
}
```
Updates the score for the specified user.

**Response:**
```json
{
  "message": "Score updated successfully",
  "data": {
    "id": 1,
    "name": "Alice",
    "score": 100
  }
}
```

### 4. Get Version
```http
GET /version
```
Returns the application version.

**Response:**
```json
{
  "version": "0.1.0"
}
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

The application reads configuration from:
1. `.env` file in the project root
2. Environment variables (higher priority)

Available settings:
- `APP_VERSION`: Application version (default: "0.1.0")
- `POSTGRES_HOST`: PostgreSQL host (default: "localhost")
- `POSTGRES_PORT`: PostgreSQL port (default: 5432)
- `POSTGRES_DB`: Database name (default: "leaderboard")
- `POSTGRES_USER`: Database user (default: "postgres")
- `POSTGRES_PASSWORD`: Database password (default: "postgres")

## Project Structure

```
leaderboard/
├── main.py           # FastAPI application and endpoints
├── config.py         # Configuration management
├── database.py       # Database connection and table creation
├── models.py         # Pydantic models
├── .env              # Environment configuration (not in version control)
├── .env.example      # Example environment configuration
├── .gitignore        # Git ignore rules
├── pyproject.toml    # Project dependencies
└── README.md         # This file
```

## Development

The application uses:
- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy 2.0** - Async ORM for database operations
- **Alembic** - Database migration tool
- **asyncpg** - Async PostgreSQL driver for Python
- **psycopg2** - Sync PostgreSQL driver (for migrations)
- **pydantic** - Data validation using Python type annotations
- **python-dotenv** - Environment variable management
- **uvicorn** - ASGI server

### Database Migrations

See [MIGRATIONS.md](MIGRATIONS.md) for detailed migration instructions.

Quick commands:
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`
- Rollback: `alembic downgrade -1`

## License

MIT
