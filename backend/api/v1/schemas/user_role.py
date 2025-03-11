from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum

# Role Enum
class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

# School Role Enum
class SchoolRoleEnum(str, Enum):
    faculty = "faculty"
    staff = "staff"
    student = "student"

# UserOut Schema (for API response)
class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    role: RoleEnum
    school_role: SchoolRoleEnum

    class Config:
        from_attributes = True
