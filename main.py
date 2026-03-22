# main.py
# FastAPI application for Task Management System
# This is the main entry point for the application

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import database and models
from database import engine, get_db, Base
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, ErrorResponse
from crud import TaskCRUD

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI(
    title="Task Management System",
    description="A FastAPI backend for managing tasks with CRUD operations",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# ============================================================================
# HEALTH AND INFO ENDPOINTS
# ============================================================================

@app.get("/", tags=["Info"])
def root():
    """
    Root endpoint - returns API information
    """
    return {
        "message": "Task Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "reference": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


# ============================================================================
# TASK ENDPOINTS
# ============================================================================

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201,
    tags=["Tasks"],
    summary="Create a new task",
    responses={
        201: {"description": "Task created successfully"},
        422: {"description": "Validation error - title cannot be empty"}
    }
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Create a new task
    
    - **title** (required): Task title (1-255 characters)
    - **description** (optional): Task description (max 1000 characters)
    
    Returns:
        - **id**: Task unique identifier
        - **title**: Task title
        - **description**: Task description
        - **completed**: Task completion status
        - **created_at**: Task creation timestamp
        - **updated_at**: Task last update timestamp
    """
    # Create the task using CRUD operation
    db_task = TaskCRUD.create_task(db=db, task=task)
    return db_task


@app.get(
    "/tasks",
    response_model=TaskListResponse,
    tags=["Tasks"],
    summary="Get all tasks with statistics",
    responses={
        200: {"description": "List of all tasks"}
    }
)
def get_all_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    Retrieve all tasks with pagination support
    
    - **skip**: Number of tasks to skip (default: 0)
    - **limit**: Maximum number of tasks to return (default: 100, max: 100)
    
    Returns:
        - **total**: Total number of tasks in database
        - **completed_count**: Number of completed tasks
        - **pending_count**: Number of pending tasks
        - **tasks**: Array of task objects
    """
    # Get all tasks and statistics
    tasks = TaskCRUD.get_all_tasks(db=db, skip=skip, limit=limit)
    stats = TaskCRUD.get_task_stats(db=db)
    
    return TaskListResponse(
        total=stats["total"],
        completed_count=stats["completed"],
        pending_count=stats["pending"],
        tasks=tasks
    )


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Get a specific task by ID",
    responses={
        200: {"description": "Task found and returned"},
        404: {"description": "Task not found"}
    }
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Retrieve a specific task by its ID
    
    - **task_id**: The unique identifier of the task to retrieve
    
    Returns the task object if found, otherwise returns 404 error
    """
    # Fetch the task
    db_task = TaskCRUD.get_task_by_id(db=db, task_id=task_id)
    
    # Check if task exists
    if not db_task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    
    return db_task


@app.get(
    "/tasks/filter/completed",
    response_model=TaskListResponse,
    tags=["Tasks"],
    summary="Get all completed tasks",
    responses={
        200: {"description": "List of completed tasks"}
    }
)
def get_completed_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    Retrieve all completed tasks with pagination
    
    - **skip**: Number of tasks to skip (default: 0)
    - **limit**: Maximum number of tasks to return (default: 100, max: 100)
    
    Returns:
        - **total**: Total number of completed tasks
        - **completed_count**: Same as total
        - **pending_count**: Always 0
        - **tasks**: Array of completed task objects
    """
    # Get completed tasks
    tasks = TaskCRUD.get_completed_tasks(db=db, skip=skip, limit=limit)
    completed_count = len(tasks)
    
    return TaskListResponse(
        total=completed_count,
        completed_count=completed_count,
        pending_count=0,
        tasks=tasks
    )


@app.get(
    "/tasks/filter/pending",
    response_model=TaskListResponse,
    tags=["Tasks"],
    summary="Get all pending tasks",
    responses={
        200: {"description": "List of pending tasks"}
    }
)
def get_pending_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    Retrieve all pending (not completed) tasks with pagination
    
    - **skip**: Number of tasks to skip (default: 0)
    - **limit**: Maximum number of tasks to return (default: 100, max: 100)
    
    Returns:
        - **total**: Total number of pending tasks
        - **completed_count**: Always 0
        - **pending_count**: Same as total
        - **tasks**: Array of pending task objects
    """
    # Get pending tasks
    tasks = TaskCRUD.get_pending_tasks(db=db, skip=skip, limit=limit)
    pending_count = len(tasks)
    
    return TaskListResponse(
        total=pending_count,
        completed_count=0,
        pending_count=pending_count,
        tasks=tasks
    )


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Update a task",
    responses={
        200: {"description": "Task updated successfully"},
        404: {"description": "Task not found"}
    }
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update an existing task
    Only provided fields will be updated; other fields remain unchanged
    
    - **task_id**: The unique identifier of the task to update
    - **title** (optional): New task title (1-255 characters)
    - **description** (optional): New task description (max 1000 characters)
    - **completed** (optional): New completion status
    
    Returns the updated task object if found, otherwise returns 404 error
    """
    # Update the task
    db_task = TaskCRUD.update_task(db=db, task_id=task_id, task_update=task_update)
    
    # Check if task exists
    if not db_task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    
    return db_task


@app.patch(
    "/tasks/{task_id}/complete",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Mark a task as completed",
    responses={
        200: {"description": "Task marked as completed"},
        404: {"description": "Task not found"}
    }
)
def mark_task_completed(
    task_id: int,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Mark a specific task as completed
    
    - **task_id**: The unique identifier of the task to mark as completed
    
    Returns the updated task object if found, otherwise returns 404 error
    """
    # Mark task as completed
    db_task = TaskCRUD.mark_completed(db=db, task_id=task_id)
    
    # Check if task exists
    if not db_task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    
    return db_task


@app.patch(
    "/tasks/{task_id}/pending",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Mark a task as pending",
    responses={
        200: {"description": "Task marked as pending"},
        404: {"description": "Task not found"}
    }
)
def mark_task_pending(
    task_id: int,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Mark a specific task as pending (not completed)
    
    - **task_id**: The unique identifier of the task to mark as pending
    
    Returns the updated task object if found, otherwise returns 404 error
    """
    # Mark task as pending
    db_task = TaskCRUD.mark_pending(db=db, task_id=task_id)
    
    # Check if task exists
    if not db_task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    
    return db_task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    tags=["Tasks"],
    summary="Delete a task",
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"description": "Task not found"}
    }
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a task from the database
    
    - **task_id**: The unique identifier of the task to delete
    
    Returns 204 No Content on success, 404 if task not found
    """
    # Delete the task
    deleted = TaskCRUD.delete_task(db=db, task_id=task_id)
    
    # Check if task was deleted
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    
    return None


# ============================================================================
# STATISTICS ENDPOINT
# ============================================================================

@app.get(
    "/stats",
    tags=["Statistics"],
    summary="Get task statistics",
    responses={
        200: {"description": "Task statistics"}
    }
)
def get_statistics(db: Session = Depends(get_db)):
    """
    Get statistics about tasks in the database
    
    Returns:
        - **total**: Total number of tasks
        - **completed**: Number of completed tasks
        - **pending**: Number of pending tasks
        - **completion_percentage**: Percentage of completed tasks (0-100)
    """
    stats = TaskCRUD.get_task_stats(db=db)
    
    # Calculate completion percentage
    completion_percentage = 0 if stats["total"] == 0 else (stats["completed"] / stats["total"]) * 100
    
    return {
        **stats,
        "completion_percentage": round(completion_percentage, 2)
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom error handler for HTTP exceptions
    """
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    # This block is for running the app directly with python main.py
    # However, it's recommended to use uvicorn command line instead
    import uvicorn
    
    print("=" * 60)
    print("Task Management System API")
    print("=" * 60)
    print("Starting server on http://127.0.0.1:8000")
    print("API Documentation: http://127.0.0.1:8000/docs (Swagger UI)")
    print("Alternative Docs: http://127.0.0.1:8000/redoc (ReDoc)")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
