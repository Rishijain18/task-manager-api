# database.py
# This module handles database configuration and session management

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator

# SQLite database URL - creates a SQLite database file named task_manager.db
DATABASE_URL = "sqlite:///./task_manager.db"

# Create the database engine
# connect_args={"check_same_thread": False} is needed for SQLite to allow
# multiple threads to access the database (required for FastAPI async operations)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()


# Dependency injection function to get database session
# This function can be injected into FastAPI route handlers using Depends()
def get_db() -> Generator:
    """
    Dependency function that provides a database session to route handlers.
    
    Yields:
        SQLAlchemy Session: A database session for the request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session after the request is complete
        db.close()
