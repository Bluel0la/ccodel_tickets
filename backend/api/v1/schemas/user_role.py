from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum

# Role Enum
class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "student"

# UserOut Schema (for API response)
class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    role: RoleEnum

    class Config:
        from_attributes = True
