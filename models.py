# models.py
# This module defines the SQLAlchemy ORM models for the Task table

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Task(Base):
    """
    Task ORM Model
    
    Represents a task in the database with the following fields:
    - id: Unique identifier for the task
    - title: Title/name of the task
    - description: Detailed description of the task
    - completed: Boolean flag indicating if the task is completed
    - created_at: Timestamp when the task was created
    - updated_at: Timestamp when the task was last updated
    """
    
    __tablename__ = "tasks"
    
    # Primary key - auto-incremented integer ID
    id = Column(Integer, primary_key=True, index=True)
    
    # Task title - required string field with maximum length
    title = Column(String(255), nullable=False, index=True)
    
    # Task description - optional text field
    description = Column(String(1000), nullable=True)
    
    # Task completion status - defaults to False (not completed)
    completed = Column(Boolean, default=False, index=True)
    
    # Timestamp of task creation - automatically set to current time
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Timestamp of last task update - automatically set and updated to current time
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
