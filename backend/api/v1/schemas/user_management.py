from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from api.v1.schemas.UserRegister import RoleEnum


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    matric_number: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[RoleEnum] = None

    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    old_password: str = Field(
        ..., min_length=8, max_length=128, description="Current password"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password, at least 8 characters",
    )

    class Config:
        from_attributes = True
