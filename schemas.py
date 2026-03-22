# schemas.py
# This module defines the Pydantic schemas for request/response validation

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """
    Base schema for Task - contains common fields for task creation and updates
    """
    title: str = Field(..., min_length=1, max_length=255, description="Task title (required, 1-255 characters)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (optional, max 1000 characters)")


class TaskCreate(TaskBase):
    """
    Schema for creating a new task
    Inherits title and description from TaskBase
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating a task
    All fields are optional to allow partial updates
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: Optional[bool] = Field(None, description="Task completion status")


class TaskResponse(TaskBase):
    """
    Schema for task response - includes all task data including database-generated fields
    Used for API responses to clients
    """
    id: int = Field(..., description="Task unique identifier")
    completed: bool = Field(..., description="Task completion status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")
    
    # Configuration for Pydantic to work with ORM models
    class Config:
             orm_mode = True  # Allows Pydantic to read ORM model attributes


class TaskListResponse(BaseModel):
    """
    Schema for list response containing multiple tasks
    """
    total: int = Field(..., description="Total number of tasks")
    completed_count: int = Field(..., description="Number of completed tasks")
    pending_count: int = Field(..., description="Number of pending tasks")
    tasks: list[TaskResponse] = Field(..., description="List of tasks")


class ErrorResponse(BaseModel):
    """
    Schema for error responses
    """
    detail: str = Field(..., description="Error message")
