from app.db.database import AsyncSessionLocal
from typing import AsyncGenerator
import httpx
from contextlib import asynccontextmanager

async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_http_client():
    client = httpx.AsyncClient(timeout=10.0)
    try:
        yield client
    finally:
        await client.aclose()


