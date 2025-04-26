from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db
from app.schemas.user import UserResponse, UserCreate
from app.schemas.auth import Login
from app.crud import user as user_crud
from app.models.user import User

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", response_model=UserResponse)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await user_crud.create_user(db, data)
    return user

@router.get("/login", response_model=UserResponse)
async def login(data: Login = Depends(), db: AsyncSession = Depends(get_db)):
    user = await user_crud.login(data, db)
    return user

@router.get("/details", response_model=UserResponse)
async def get_user_details(current_user: User = Depends(user_crud.get_current_user)):
    return current_user


