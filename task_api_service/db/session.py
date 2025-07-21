from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=True,
    connect_args={"check_same_thread": False}  # required for SQLite
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Give access to the DB session for the duration of the request
async def get_db():
    async with SessionLocal() as session:
        yield session
