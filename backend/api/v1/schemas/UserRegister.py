from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "student"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    firstname: str = Field(..., min_length=1, max_length=50)
    lastname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        str_strip_whitespace = True


class UserSignin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        str_strip_whitespace = True

class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    role: RoleEnum

    class Config:
        from_attributes = True
