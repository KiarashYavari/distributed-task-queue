from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from db.session import AsyncSessionLocal
from db.models import Task
from processor.handlers import process_echo, process_reverse, process_cpu_intensive
from utiles.logger import logger
from uuid import UUID

router = APIRouter()

# going to call relevent process for each task
PROCESSORS = {
    "echo": process_echo,
    "reverse_string": process_reverse,
    "cpu_intensive": process_cpu_intensive,
}

@router.post("/process-task/{task_id}", status_code=200, summary="Process a pending task",
             description="Fetches a task by its ID, validates its state,\
                 processes it according to the task type, and stores the result.",
                     responses={
                                200: {"description": "Task processed successfully"},
                                400: {"description": "Task not in pending state or invalid"},
                                404: {"description": "Task not found"},
                                500: {"description": "Internal processing error"},
                            },
            )
async def process_task(task_id: UUID):
    """Going to process created tasks with pending status

    Args:
        request (TaskProcessRequest): need the task_id to retrieve it from db

    Raises:
        HTTPException: for invalid inputs in task
        ValueError: un defined task type is sent

    Returns:
        JSON: task status and task result
    """
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task:
            logger.info("task not found in db!")
            raise HTTPException(status_code=404, detail="Task not found")

        if task.status != "pending":
            raise HTTPException(status_code=400, detail=f"Task status is '{task.status}', cannot process")

        task.status = "in_progress"
        await session.commit()

        try:
            processor = PROCESSORS.get(task.task_type)
            if not processor:
                raise ValueError(f"Unknown task_type: {task.task_type}")

            task.result = await processor(task.payload)
            task.status = "completed"
            logger.info(f"Task {task.id} completed successfully.")

        except Exception as e:
            task.status = "failed"
            task.result = str(e)
            logger.error(f"Task {task.id} failed with error: {e}")

        finally:
            session.add(task)
            await session.commit()

    return {"status": task.status, "result": task.result}
