from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Task
from schemas import TaskCreate, TaskUpdate


class TaskCRUD:

    @staticmethod
    def create_task(db: Session, task: TaskCreate) -> Task:
        db_task = Task(
            title=task.title,
            description=task.description
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_all_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        stmt = select(Task).order_by(Task.created_at.desc()).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Task | None:
        return db.get(Task, task_id)

    @staticmethod
    def get_completed_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        stmt = (
            select(Task)
            .where(Task.completed.is_(True))
            .order_by(Task.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    @staticmethod
    def get_pending_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        stmt = (
            select(Task)
            .where(Task.completed.is_(False))
            .order_by(Task.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task | None:
        db_task = db.get(Task, task_id)

        if not db_task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_task, field, value)

        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def mark_completed(db: Session, task_id: int) -> Task | None:
        db_task = db.get(Task, task_id)

        if not db_task:
            return None

        db_task.completed = True
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def mark_pending(db: Session, task_id: int) -> Task | None:
        db_task = db.get(Task, task_id)

        if not db_task:
            return None

        db_task.completed = False
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        db_task = db.get(Task, task_id)

        if not db_task:
            return False

        db.delete(db_task)
        db.commit()
        return True

    @staticmethod
    def get_task_stats(db: Session) -> dict:
        total = db.query(Task).count()
        completed = db.query(Task).filter(Task.completed.is_(True)).count()
        pending = total - completed

        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }