from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

class SchoolRole(str, Enum):
    student = "student"
    faculty = "faculty"
    staff = "staff"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    firstname: str = Field(..., min_length=1, max_length=50)
    lastname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    school_role: SchoolRole  # User must provide one of the valid roles

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
    school_role: SchoolRole

    class Config:
        from_attributes = True
