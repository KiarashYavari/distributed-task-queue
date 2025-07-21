from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    status = Column(String, default="pending", nullable=False)
    result = Column(Text, nullable=True)
