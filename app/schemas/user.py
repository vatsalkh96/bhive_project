# app/schemas/user.py
from pydantic import BaseModel, ConfigDict, EmailStr, Field
import datetime
from typing import Annotated
from uuid import UUID


PASSWORD_REGEX = r'^[A-Za-z\d[^A-Za-z0-9]]{8,}$'

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8, pattern = PASSWORD_REGEX)]
    first_name: str
    last_name: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime.datetime
    needs_relogin: bool
    last_login: datetime.datetime

    model_config = ConfigDict(
        from_attributes=True,  # Enables conversion from SQLAlchemy models
        populate_by_name=True
    )



class UserPatch(BaseModel):
    password: Annotated[str|None, Field(min_length=16, pattern = PASSWORD_REGEX)]