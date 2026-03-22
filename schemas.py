from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    total: int
    completed_count: int
    pending_count: int
    tasks: list[TaskResponse]


class ErrorResponse(BaseModel):
    detail: str