from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import settings
from .base import Base

# Create the async engine
async_engine = create_async_engine(settings.async_database_url, echo=False, future=True)

# Create an async sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# # Dependency for FastAPI routes
# async def get_db() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         yield session

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

