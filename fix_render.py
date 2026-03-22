import yaml
from pathlib import Path

content = '''# schemas.py
# Pydantic v1 compatible schemas for FastAPI Task Management System

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
'''

(Path('schemas.py')).write_text(content, encoding='utf-8')

render_file = Path('render.yaml')
if render_file.exists():
    data = yaml.safe_load(render_file.read_text(encoding='utf-8'))
    if 'services' in data and isinstance(data['services'], list) and data['services']:
        data['services'][0]['runtime'] = 'python-3.11'
        envVars = [v for v in data['services'][0].get('envVars', []) if v.get('key') != 'PYTHON_VERSION']
        envVars.append({'key': 'PYTHON_VERSION', 'value': '3.11.7'})
        data['services'][0]['envVars'] = envVars
    render_file.write_text(yaml.dump(data, sort_keys=False), encoding='utf-8')

Path('.python-version').write_text('3.11.7\n', encoding='utf-8')
print('✅ Updated schemas.py, render.yaml, .python-version')