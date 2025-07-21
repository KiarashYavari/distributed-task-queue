from fastapi import FastAPI
from api.routes import router
from utiles.logger import logger
from db.session import engine
from db.models import Base

app = FastAPI(title="Task API Service")

app.include_router(router)

@app.on_event("startup")
async def on_startup():
    logger.info("Task API Service started")
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created or already exist.")
