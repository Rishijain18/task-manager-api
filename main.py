# main.py

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from crud import TaskCRUD
from auth import hash_password, verify_password, create_access_token
from models import User
from schemas import UserCreate, UserLogin, Token

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="Task Management System",
    description="A FastAPI backend for managing tasks with CRUD operations",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT + HEALTH
# =========================

@app.get("/")
def root():
    return {
        "message": "Task Management System API",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# =========================
# TASK APIs
# =========================

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return TaskCRUD.create_task(db, task)


@app.get("/tasks", response_model=TaskListResponse)
def get_all_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    tasks = TaskCRUD.get_all_tasks(db, skip, limit)
    stats = TaskCRUD.get_task_stats(db)

    return TaskListResponse(
        total=stats["total"],
        completed_count=stats["completed"],
        pending_count=stats["pending"],
        tasks=tasks
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskCRUD.get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.get("/tasks/filter/completed", response_model=TaskListResponse)
def get_completed_tasks(db: Session = Depends(get_db)):
    tasks = TaskCRUD.get_completed_tasks(db)
    count = len(tasks)

    return TaskListResponse(
        total=count,
        completed_count=count,
        pending_count=0,
        tasks=tasks
    )


@app.get("/tasks/filter/pending", response_model=TaskListResponse)
def get_pending_tasks(db: Session = Depends(get_db)):
    tasks = TaskCRUD.get_pending_tasks(db)
    count = len(tasks)

    return TaskListResponse(
        total=count,
        completed_count=0,
        pending_count=count,
        tasks=tasks
    )


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = TaskCRUD.update_task(db, task_id, task_update)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def mark_completed(task_id: int, db: Session = Depends(get_db)):
    task = TaskCRUD.mark_completed(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}/pending", response_model=TaskResponse)
def mark_pending(task_id: int, db: Session = Depends(get_db)):
    task = TaskCRUD.mark_pending(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = TaskCRUD.delete_task(db, task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return None


# =========================
# STATS
# =========================

@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    stats = TaskCRUD.get_task_stats(db)

    percentage = 0 if stats["total"] == 0 else (stats["completed"] / stats["total"]) * 100

    return {
        **stats,
        "completion_percentage": round(percentage, 2)
    }


# =========================
# ERROR HANDLER (FIXED)
# =========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created"}

@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}