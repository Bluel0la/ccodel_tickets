from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, example="John Doe")
    last_name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    is_active: Optional[bool] = Field(None, example=True)


    class Config:
        from_attributes = True

class ChangePassword(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=128, description="Current password of the user")
    new_password: str = Field(
    ...,
    min_length=8,
    pattern=r"^[A-Za-z\d]{8,}$",
    description="New password (at least 8 characters, 1 letter, 1 number)"
    )


    class Config:
        from_attributes = True
