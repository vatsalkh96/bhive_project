from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import user, portfolio, scheme, health
from app.db.database import init_db
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request

from app.utils.exceptions import AppBaseException

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

router = FastAPI(lifespan=lifespan)



router.include_router(user.router)
router.include_router(portfolio.router)
router.include_router(scheme.router)
router.include_router(health.router)

@router.exception_handler(AppBaseException)
async def app_base_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

