from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# Create Async Database Engine
async_engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)

# Create Async Session Factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
