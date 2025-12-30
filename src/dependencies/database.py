from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import AsyncSessionLocal


async def get_db() -> AsyncSession:
    """Dependency function to provide an async database session"""
    async with AsyncSessionLocal() as session:
        yield session
