# crud.py
# This module contains all Create, Read, Update, Delete operations for tasks

from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate


class TaskCRUD:
    """
    CRUD operations for Task management
    All methods interact directly with the database through SQLAlchemy
    """
    
    @staticmethod
    def create_task(db: Session, task: TaskCreate) -> Task:
        """
        Create a new task in the database
        
        Args:
            db: SQLAlchemy database session
            task: TaskCreate schema with task data
            
        Returns:
            Task: The created task ORM object
        """
        # Create a new Task instance from the schema
        db_task = Task(
            title=task.title,
            description=task.description
        )
        # Add the task to the session
        db.add(db_task)
        # Commit the transaction to save to database
        db.commit()
        # Refresh to get the auto-generated fields (id, created_at, updated_at)
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def get_all_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        """
        Retrieve all tasks from the database with pagination support
        
        Args:
            db: SQLAlchemy database session
            skip: Number of tasks to skip (for pagination)
            limit: Maximum number of tasks to return (for pagination)
            
        Returns:
            list[Task]: List of task ORM objects ordered by creation date (newest first)
        """
        return db.query(Task).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Task | None:
        """
        Retrieve a specific task by its ID
        
        Args:
            db: SQLAlchemy database session
            task_id: The ID of the task to retrieve
            
        Returns:
            Task | None: The task ORM object if found, None otherwise
        """
        return db.query(Task).filter(Task.id == task_id).first()
    
    @staticmethod
    def get_completed_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        """
        Retrieve all completed tasks from the database
        
        Args:
            db: SQLAlchemy database session
            skip: Number of tasks to skip (for pagination)
            limit: Maximum number of tasks to return (for pagination)
            
        Returns:
            list[Task]: List of completed task ORM objects
        """
        return db.query(Task).filter(Task.completed == True).order_by(Task.updated_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_pending_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        """
        Retrieve all pending (not completed) tasks from the database
        
        Args:
            db: SQLAlchemy database session
            skip: Number of tasks to skip (for pagination)
            limit: Maximum number of tasks to return (for pagination)
            
        Returns:
            list[Task]: List of pending task ORM objects
        """
        return db.query(Task).filter(Task.completed == False).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task | None:
        """
        Update an existing task with new data
        Only updates fields that are provided (not None)
        
        Args:
            db: SQLAlchemy database session
            task_id: The ID of the task to update
            task_update: TaskUpdate schema with fields to update
            
        Returns:
            Task | None: The updated task ORM object if found, None otherwise
        """
        # Fetch the task from database
        db_task = db.query(Task).filter(Task.id == task_id).first()
        
        if not db_task:
            return None
        
        # Update only the fields that are provided (not None)
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        # Commit the changes to database
        db.commit()
        # Refresh to get the updated timestamps
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def mark_completed(db: Session, task_id: int) -> Task | None:
        """
        Mark a task as completed
        
        Args:
            db: SQLAlchemy database session
            task_id: The ID of the task to mark as completed
            
        Returns:
            Task | None: The updated task ORM object if found, None otherwise
        """
        db_task = db.query(Task).filter(Task.id == task_id).first()
        
        if not db_task:
            return None
        
        db_task.completed = True
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def mark_pending(db: Session, task_id: int) -> Task | None:
        """
        Mark a task as pending (not completed)
        
        Args:
            db: SQLAlchemy database session
            task_id: The ID of the task to mark as pending
            
        Returns:
            Task | None: The updated task ORM object if found, None otherwise
        """
        db_task = db.query(Task).filter(Task.id == task_id).first()
        
        if not db_task:
            return None
        
        db_task.completed = False
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        """
        Delete a task from the database
        
        Args:
            db: SQLAlchemy database session
            task_id: The ID of the task to delete
            
        Returns:
            bool: True if task was deleted, False if task was not found
        """
        db_task = db.query(Task).filter(Task.id == task_id).first()
        
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True
    
    @staticmethod
    def get_task_stats(db: Session) -> dict:
        """
        Get statistics about tasks in the database
        
        Args:
            db: SQLAlchemy database session
            
        Returns:
            dict: Dictionary containing total, completed, and pending task counts
        """
        total_tasks = db.query(Task).count()
        completed_tasks = db.query(Task).filter(Task.completed == True).count()
        pending_tasks = total_tasks - completed_tasks
        
        return {
            "total": total_tasks,
            "completed": completed_tasks,
            "pending": pending_tasks
        }
