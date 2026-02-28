import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
from typing import List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import db
from db_models import LeaderboardUser
from models import (
    LeaderboardEntry,
    AddUserRequest,
    UpdateScoreRequest,
    VersionResponse,
    MessageResponse
)
from auth import verify_api_key, verify_admin_api_key


async def get_db_session() -> AsyncSession:
    """Dependency to get database session"""
    async for session in db.get_session():
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup: Connect to database
    await db.connect()
    yield
    # Shutdown: Disconnect from database
    await db.disconnect()


# Initialize FastAPI application
app = FastAPI(
    title="Leaderboard API",
    description="""
    ## Leaderboard Backend Application
    
    A high-performance leaderboard API built with FastAPI, SQLAlchemy ORM, and PostgreSQL.
    
    ### Features
    * **List Leaderboard** - Get all users sorted by score
    * **Add Users** - Register new users with initial score of 0
    * **Update Scores** - Update user scores by name
    * **Delete Users** - Remove users (admin only)
    * **Version Info** - Get application version
    * **API Key Authentication** - Secure endpoints with API key
    * **Role-Based Access** - Separate admin API key for privileged operations
    
    ### Technology Stack
    * FastAPI - Modern async web framework
    * SQLAlchemy 2.0 - Async ORM
    * Alembic - Database migrations
    * PostgreSQL - Database
    * Pydantic - Data validation
    
    ### Authentication
    
    **Two levels of API keys:**
    
    1. **Regular API Key** (`X-API-Key` header)
       - Access to most endpoints
       - List leaderboard, add users, update scores
    
    2. **Admin API Key** (`X-Admin-API-Key` header)
       - Access to privileged operations
       - Delete users
    
    **Public endpoints (no authentication required):**
    * `GET /` - Welcome message
    * `GET /version` - API version
    
    **Example Headers:**
    ```
    X-API-Key: your-secret-api-key-change-this
    X-Admin-API-Key: your-admin-api-key-change-this
    ```
    """,
    version=settings.app_version,
    lifespan=lifespan,
    contact={
        "name": "Leaderboard API Support",
        "email": "y.sukhorukov.uav@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    tags_metadata=[
        {
            "name": "leaderboard",
            "description": "Operations to manage and view the leaderboard",
        },
        {
            "name": "users",
            "description": "User management operations - add and update users",
        },
        {
            "name": "system",
            "description": "System information and health check endpoints",
        },
    ],
)


@app.get(
    "/",
    response_model=MessageResponse,
    tags=["system"],
    summary="Welcome endpoint",
    description="Returns a welcome message and current API version",
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Welcome to Leaderboard API",
                        "data": {"version": "0.1.0"}
                    }
                }
            }
        }
    }
)
async def root():
    """Root endpoint"""
    return MessageResponse(
        message="Welcome to Leaderboard API",
        data={"version": settings.app_version}
    )


@app.get(
    "/leaderboard",
    response_model=List[LeaderboardEntry],
    tags=["leaderboard"],
    summary="Get leaderboard rankings",
    description="""
    Retrieve the complete leaderboard with all users sorted by score.
    
    **Authentication Required:** API Key via `X-API-Key` header
    
    **Sorting:**
    - Primary: Score (highest to lowest)
    - Secondary: Created date (oldest first for tie-breaking)
    
    **Returns:**
    A list of all users with their scores, IDs, and timestamps.
    """,
    responses={
        200: {
            "description": "List of users in the leaderboard",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Alice",
                            "score": 300,
                            "created_at": "2026-02-28T10:00:00",
                            "updated_at": "2026-02-28T15:30:00"
                        },
                        {
                            "id": 2,
                            "name": "Bob",
                            "score": 250,
                            "created_at": "2026-02-28T10:05:00",
                            "updated_at": "2026-02-28T14:20:00"
                        },
                        {
                            "id": 3,
                            "name": "Charlie",
                            "score": 175,
                            "created_at": "2026-02-28T10:10:00",
                            "updated_at": "2026-02-28T13:15:00"
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Missing API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Missing API Key. Please provide X-API-Key header."
                    }
                }
            }
        },
        403: {
            "description": "Invalid API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API Key. Access denied."
                    }
                }
            }
        }
    }
)
async def list_leaderboard(
    session: AsyncSession = Depends(get_db_session),
    api_key: str = Depends(verify_api_key)
):
    """
    List all users in the leaderboard ordered by score (highest to lowest)
    """
    # ...existing code...
    # Query using SQLAlchemy ORM
    result = await session.execute(
        select(LeaderboardUser).order_by(LeaderboardUser.score.desc(), LeaderboardUser.created_at.asc())
    )
    users = result.scalars().all()

    return [
        LeaderboardEntry(
            id=user.id,
            name=user.name,
            score=user.score,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]


@app.post(
    "/user",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Add a new user",
    description="""
    Register a new user to the leaderboard.
    
    **Authentication Required:** API Key via `X-API-Key` header
    
    **Initial State:**
    - Score is set to 0
    - Timestamps are set to current time
    
    **Constraints:**
    - Username must be unique
    - Username must be 1-255 characters
    
    **Returns:**
    Confirmation message with user details.
    """,
    responses={
        201: {
            "description": "User successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User added successfully",
                        "data": {
                            "id": 1,
                            "name": "Alice",
                            "score": 0
                        }
                    }
                }
            }
        },
        401: {
            "description": "Missing API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Missing API Key. Please provide X-API-Key header."
                    }
                }
            }
        },
        403: {
            "description": "Invalid API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API Key. Access denied."
                    }
                }
            }
        },
        409: {
            "description": "User already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with name 'Alice' already exists"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "name"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def add_user(
    request: AddUserRequest,
    session: AsyncSession = Depends(get_db_session),
    api_key: str = Depends(verify_api_key)
):
    """
    Add a new user to the leaderboard with initial score of 0
    """
    # ...existing code...
    try:
        # Check if user already exists
        result = await session.execute(
            select(LeaderboardUser).where(LeaderboardUser.name == request.name)
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with name '{request.name}' already exists"
            )

        # Create new user
        new_user = LeaderboardUser(
            name=request.name,
            score=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return MessageResponse(
            message="User added successfully",
            data={
                "id": new_user.id,
                "name": new_user.name,
                "score": new_user.score
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add user: {str(e)}"
        )


@app.put(
    "/user/score",
    response_model=MessageResponse,
    tags=["users"],
    summary="Update user score",
    description="""
    Updates the score for an existing user identified by name.
    
    **Authentication Required:** API Key via `X-API-Key` header
    
    **Updates:**
    - Score is set to the new value
    - `updated_at` timestamp is updated automatically
    
    **Requirements:**
    - User must exist in the leaderboard
    - Score must be non-negative (≥ 0)
    
    **Returns:**
    Confirmation message with updated user details.
    """,
    responses={
        200: {
            "description": "Score successfully updated",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Score updated successfully",
                        "data": {
                            "id": 1,
                            "name": "Alice",
                            "score": 100
                        }
                    }
                }
            }
        },
        401: {
            "description": "Missing API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Missing API Key. Please provide X-API-Key header."
                    }
                }
            }
        },
        403: {
            "description": "Invalid API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API Key. Access denied."
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with name 'NonExistentUser' not found"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "score"],
                                "msg": "ensure this value is greater than or equal to 0",
                                "type": "value_error.number.not_ge"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def update_score(
    request: UpdateScoreRequest,
    session: AsyncSession = Depends(get_db_session),
    api_key: str = Depends(verify_api_key)
):
    """
    Update the score of a user by name
    """
    # ...existing code...
    try:
        # Find the user
        result = await session.execute(
            select(LeaderboardUser).where(LeaderboardUser.name == request.name)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with name '{request.name}' not found"
            )

        # Update the score
        user.score = request.score
        user.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(user)

        return MessageResponse(
            message="Score updated successfully",
            data={
                "id": user.id,
                "name": user.name,
                "score": user.score
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update score: {str(e)}"
        )


@app.delete(
    "/user/{name}",
    response_model=MessageResponse,
    tags=["users"],
    summary="Delete a user (Admin only)",
    description="""
    Delete a user from the leaderboard by name.
    
    **⚠️ Admin Authentication Required:** Admin API Key via `X-Admin-API-Key` header
    
    This is a privileged operation that requires admin-level access.
    Regular API keys (`X-API-Key`) will not work for this endpoint.
    
    **Action:**
    - Permanently removes the user from the leaderboard
    - All user data including scores and timestamps are deleted
    
    **Returns:**
    Confirmation message with deleted user details.
    """,
    responses={
        200: {
            "description": "User successfully deleted",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User deleted successfully",
                        "data": {
                            "id": 1,
                            "name": "Alice",
                            "score": 100
                        }
                    }
                }
            }
        },
        401: {
            "description": "Missing Admin API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Missing Admin API Key. Please provide X-Admin-API-Key header."
                    }
                }
            }
        },
        403: {
            "description": "Invalid Admin API Key",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid Admin API Key. Access denied. Admin privileges required."
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User with name 'NonExistentUser' not found"
                    }
                }
            }
        }
    }
)
async def delete_user(
    name: str,
    session: AsyncSession = Depends(get_db_session),
    admin_api_key: str = Depends(verify_admin_api_key)
):
    """
    Delete a user from the leaderboard (requires admin API key)
    """
    try:
        # Find the user
        result = await session.execute(
            select(LeaderboardUser).where(LeaderboardUser.name == name)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with name '{name}' not found"
            )

        # Store user data before deletion for response
        user_data = {
            "id": user.id,
            "name": user.name,
            "score": user.score
        }

        # Delete the user
        await session.delete(user)
        await session.commit()

        return MessageResponse(
            message="User deleted successfully",
            data=user_data
        )
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )


@app.get(
    "/version",
    response_model=VersionResponse,
    tags=["system"],
    summary="Get API version",
    description="""
    Returns the current version of the Leaderboard API.
    
    The version is configured via the `APP_VERSION` environment variable or `.env` file.
    """,
    responses={
        200: {
            "description": "Current API version",
            "content": {
                "application/json": {
                    "example": {
                        "version": "0.1.0"
                    }
                }
            }
        }
    }
)
async def get_version():
    """
    Return the application version from configuration
    """
    return VersionResponse(version=settings.app_version)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)