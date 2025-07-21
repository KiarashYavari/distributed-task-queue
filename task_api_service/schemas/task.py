# make sure we get one of the three defined tasks

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class TaskCreateSchema(BaseModel):
    task_type: str = Field(..., description="Type of task", example="echo")
    payload: str = Field(..., description="strin send to be processed based on task type", example="hello")