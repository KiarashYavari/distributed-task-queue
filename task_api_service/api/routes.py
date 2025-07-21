from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from db.session import get_db
from db.models import Task, TaskStatus
from services.worker_client import notify_worker
from schemas.task import TaskCreateSchema
from sqlalchemy.future import select
from uuid import UUID
from utiles.logger import logger

router = APIRouter()

ALLOWED_TASK_TYPES = {"echo", "reverse_string", "cpu_intensive"}

@router.post("/tasks", status_code=202,
                 summary="Create a new task",
                 response_description="Returns the created task's ID",
                 responses={
                                202: {"description": "Task accepted and created successfully"},
                                400: {"description": "Invalid input or unsupported task type"},
                                500: {"description": "Internal server error"},
                            }
            ,)
async def create_task(task: TaskCreateSchema, db: AsyncSession = Depends(get_db)):
    task_type = task.task_type
    payload = task.payload

    logger.info("start validation on input data!")
    if not task_type or not isinstance(payload, str) :
        raise HTTPException(status_code=400, detail="Invalid task_type or payload")
    
    if task_type not in ALLOWED_TASK_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported task_type: '{task_type}'. Must be one of: {', '.join(ALLOWED_TASK_TYPES)}"
        )
        
    logger.info("start saving the task on db!")
    task = Task(task_type=task_type, payload=payload)
    db.add(task)
    
    try:
        await db.commit()
        await db.refresh(task)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save task to DB")

    if not task.id:
        logger.error("Task ID is None after refresh!")
        raise HTTPException(status_code=500, detail="Task not properly saved")

    logger.info(f"Task saved with ID: {task.id}")
    logger.info("Calling notifier to worker service!")
    
    logger.info("going to call the notifier to worker service!")
    if task_type == "cpu_intensive":
        await notify_worker(str(task.id), intensive_task=True)
    else:
        await notify_worker(str(task.id), intensive_task=False)
    return {"task_id": str(task.id)}

@router.get("/tasks/{task_id}", status_code=200,
                summary="Get task status and result by ID",
                response_description="Returns task details",
                responses={
                    200: {"description": "Task found and returned"},
                    404: {"description": "Task not found"},
                },
            )
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    """
        Retrieve task status and result using task ID.

        Args:
            task_id (UUID): Unique task identifier

        Returns:
            JSON: task_id, status, and result
    """
    try:
        logger.info(f"Fetching task_id: {task_id}")
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            logger.warning(f"Task {task_id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Defensive logging for debugging
        logger.info(f"Task found: id={task.id}, status={task.status}, result={task.result}")
        
        # Try to return JSON response safely
        response = {
            "task_id": str(task.id),
            "status": task.status,
            "result": task.result,
        }
        return response

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching task: {e}")
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        logger.exception(f"Unexpected error while retrieving task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
