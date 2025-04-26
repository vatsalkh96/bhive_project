import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from app.models import User
from app.schemas.common import SuccessResponse
from app.schemas.user import UserCreate, UserPatch, UserResponse
from app.schemas.auth import Login
from app.utils.helpers import create_hash, utcnow
from fastapi import Depends, Header
from app.deps import get_db
from app.utils.exceptions import BadRequestException, NotFoundException, UnauthorizedException


async def get_current_user(
    x_user_id: str | None = Header(..., example='585855e8-d92e-4d56-bdee-3bed16b68b11'),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    
    if not x_user_id:
        raise BadRequestException('Essentials headers missing')

    user = (await db.execute(select(User).where(User.id == x_user_id))).scalars().first()
    if not user:
        raise NotFoundException('User not found.')
    
    return user


async def login(data: Login, db: AsyncSession) -> UserResponse:
    user = (
        await db.execute(
            select(User)
            .where(
                User.email == data.email,
            )
        )
    ).scalar_one_or_none()

    if not user:
        raise NotFoundException('This email is not registered. Please sign up')
    
    if not user.verify_password(data.password):
        raise UnauthorizedException('Wrong password. Please enter correct password.')
    
    user.last_login = utcnow()
    await db.commit()
    await db.refresh(user)

    return UserResponse.model_validate(user)


async def create_user(db: AsyncSession, data: UserCreate) -> UserResponse:
    user = User(email=data.email, hashed_password=create_hash(data.password), first_name = data.first_name, last_name = data.last_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)


async def update_user(user: User, db: AsyncSession, data: UserPatch)-> SuccessResponse:
    if data.password:
        user.set_password(data.password)    
    await db.commit()

    return SuccessResponse(message='Updated details')