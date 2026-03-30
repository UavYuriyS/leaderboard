# Leaderboard Backend Application

A simple leaderboard backend API built with FastAPI and PostgreSQL.

## Quick Start

Just run it with Docker Compose:
```bash
   docker-compose up -d
```

5. **Test the API**:
   - **Interactive Swagger UI:** http://localhost:8000/docs
   - **ReDoc Documentation:** http://localhost:8000/redoc
   - Or run the test script: `python test_api.py`

## Features

- **List leaderboard** - Get all users sorted by score (highest to lowest)
- **Add users** - Register new users with initial score of 0
- **Update scores** - Modify user scores by matching `uid` + name
- **Delete users** - Remove users (admin only)
- **Get version** - Retrieve current API version
- **API Key Authentication** - Two-tier authentication (regular + admin)
- **Interactive API Documentation** - Full Swagger/OpenAPI documentation
- **SQLAlchemy ORM** - Type-safe database operations
- **Alembic Migrations** - Version-controlled database schema (auto-applied on startup)
- **PostgreSQL database** - Async connection pooling
- **Fully Dockerized** - One-command deployment
- **Environment Configuration** - .env file with environment variable override

## Prerequisites

- Docker and Docker Compose installed on your machine

## Installation

1. . Configure the app:
   - Copy `.env.example` to `.env`
   - Update the PostgreSQL connection settings in `.env` and API keys

2. Start the application:
   ```bash
   docker-compose up -d
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

## API Endpoints

All endpoints except `/` and `/version` require authentication via API keys.

### Authentication Headers

**Regular API Key** (for most operations):
```
X-API-Key: your-secret-api-key-change-this
```

**Admin API Key** (for delete operations):
```
X-Admin-API-Key: your-admin-api-key-change-this
```

### 1. List Leaderboard
```http
GET /leaderboard
X-API-Key: your-secret-api-key-change-this
?uid=u-1001
```
Returns all users ordered by score (highest to lowest). The `uid` must belong to an existing user.

**Response:**
```json
[
  {
    "id": 1,
    "uid": "u-1001",
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
X-API-Key: your-secret-api-key-change-this
Content-Type: application/json

{
  "uid": "u-1001",
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
    "uid": "u-1001",
    "name": "Alice",
    "score": 0
  }
}
```

### 3. Update Score
```http
PUT /user/score
X-API-Key: your-secret-api-key-change-this
Content-Type: application/json

{
  "uid": "u-1001",
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
    "uid": "u-1001",
    "name": "Alice",
    "score": 100
  }
}
```

### 4. Delete User (Admin Only)
```http
DELETE /user/Alice
X-Admin-API-Key: your-admin-api-key-change-this
```
Deletes a user from the leaderboard. **Requires admin API key.**

**Response:**
```json
{
  "message": "User deleted successfully",
  "data": {
    "id": 1,
    "name": "Alice",
    "score": 100
  }
}
```

### 5. Get Version
```http
GET /version
```
Returns the application version. **No authentication required.**

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
- `API_KEY`: API key for protected endpoints
- `ADMIN_API_KEY` API key for admin endpoints

## License

MIT
