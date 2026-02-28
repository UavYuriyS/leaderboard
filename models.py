from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class LeaderboardEntry(BaseModel):
    """Model for a leaderboard entry"""
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Alice",
                "score": 250,
                "created_at": "2026-02-28T10:00:00",
                "updated_at": "2026-02-28T15:30:00"
            }
        }
    )

    id: int = Field(..., description="Unique user ID", examples=[1, 2, 3])
    name: str = Field(..., description="User's unique name", examples=["Alice", "Bob", "Charlie"])
    score: int = Field(..., description="User's current score", examples=[100, 250, 500])
    created_at: datetime = Field(..., description="Timestamp when user was created")
    updated_at: datetime = Field(..., description="Timestamp when user was last updated")


class AddUserRequest(BaseModel):
    """Request model for adding a user"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alice"
            }
        }
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="User's unique name (1-255 characters)",
        examples=["Alice", "Bob", "Charlie", "Player123"]
    )


class UpdateScoreRequest(BaseModel):
    """Request model for updating a user's score"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Alice",
                "score": 100
            }
        }
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the user to update",
        examples=["Alice", "Bob", "Charlie"]
    )
    score: int = Field(
        ...,
        ge=0,
        description="New score for the user (must be ≥ 0)",
        examples=[0, 50, 100, 500, 1000]
    )


class VersionResponse(BaseModel):
    """Response model for version endpoint"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "version": "0.1.0"
            }
        }
    )

    version: str = Field(..., description="Current API version", examples=["0.1.0", "1.0.0"])


class MessageResponse(BaseModel):
    """Generic message response"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation successful",
                "data": {"id": 1, "name": "Alice", "score": 100}
            }
        }
    )

    message: str = Field(..., description="Human-readable message", examples=["User added successfully", "Score updated successfully"])
    data: Optional[dict] = Field(None, description="Additional data related to the operation")
