import httpx
from core.config import settings
from loguru import logger

async def notify_worker(task_id: str, intensive_task: bool=False):
    """_summary_
        sends a POST to /process-task and start task process on worker service
    Args:
        task_id (str):send the task id for the new task that needs to be executed
    """
    try:
        async with httpx.AsyncClient() as client:
            if intensive_task:
                logger.info("doing notify request with extended timeout!")
                res = await client.post(f"{settings.worker_url}/process-task/{task_id}", timeout=15.0)
            else:
                res = await client.post(f"{settings.worker_url}/process-task/{task_id}",)
            res.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to notify worker: {e}")
        raise
