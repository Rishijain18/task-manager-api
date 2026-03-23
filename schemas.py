# schemas.py
# This module defines the Pydantic schemas for request/response validation
# Updated for Pydantic v1.10.7 compatibility with Python 3.11.7

from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

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

    @validator('description')
    def description_max_length(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip() if v is not None else v

    @validator('title')
    def title_max_length(cls, v):
        if v is not None and len(v) > 255:
            raise ValueError('Title must be 255 characters or less')
        return v

    @validator('description')
    def description_max_length(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v


class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    limit: int


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    
class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str