# schemas.py
# This module defines the Pydantic schemas for request/response validation
# Updated for Pydantic v1.10.7 compatibility with Python 3.11.7

from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    """
    Base schema for Task - contains common fields for task creation and updates
    """
    title = ...  # Required field
    description = None  # Optional field

    class Config:
        arbitrary_types_allowed = True

    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('title')
    def title_max_length(cls, v):
        if len(v) > 255:
            raise ValueError('Title must be 255 characters or less')
        return v


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
    title: Union[str, None] = None
    description: Union[str, None] = None
    completed: Union[bool, None] = None

    @validator('title')
    def title_not_empty_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v

    @validator('title')
    def title_max_length(cls, v):
        if v and len(v) > 255:
            raise ValueError('Title must be 255 characters or less')
        return v

    @validator('description')
    def description_max_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v


class TaskResponse(TaskBase):
    """
    Schema for task response - includes all task data including database-generated fields
    Used for API responses to clients
    """
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        # Pydantic v1 config for ORM integration
        orm_mode = True


class TaskListResponse(BaseModel):
    """
    Schema for list response containing multiple tasks
    """
    total: int
    completed_count: int
    pending_count: int
    tasks: List[TaskResponse]


class ErrorResponse(BaseModel):
    """
    Schema for error responses
    """
    detail: str