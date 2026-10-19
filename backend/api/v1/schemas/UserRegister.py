from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    student = "student"


class UserCreate(BaseModel):
    matric_number: str = Field(..., min_length=3, max_length=50)
    firstname: str = Field(..., min_length=1, max_length=50)
    lastname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        str_strip_whitespace = True


class AdminUserCreate(UserCreate):
    role: RoleEnum = RoleEnum.student


class UserSignin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        str_strip_whitespace = True


class UserOut(BaseModel):
    user_id: UUID
    matric_number: Optional[str] = None
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleEnum
    is_active: bool = True
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True
