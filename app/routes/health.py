from fastapi import APIRouter, Depends
from app.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/live")
async def liveness_check():
    return {"status": "alive"}

@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return {"status": "db_not_ready"}
