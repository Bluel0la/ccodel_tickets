from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.utils.user_service import get_all_users
from api.v1.schemas.UserRegister import UserOut
from api.v1.schemas.user_management import UserUpdate, ChangePassword
from api.utils.authentication import get_current_user, is_admin
from api.utils.user_service import get_user_by_id, update_user_details, soft_delete_user, change_password
from typing import List
from uuid import UUID

user = APIRouter(prefix="/users", tags=["Users"])

@user.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    return get_all_users(db)

@user.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not is_admin(current_user) and current_user["user_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Access denied")
    return get_user_by_id(db, user_id)


@user.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not is_admin(current_user) and current_user["id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Access denied")
    return update_user_details(db, user_id, user_data)


@user.delete("/{user_id}")
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    return soft_delete_user(db, user_id)


@user.put("/change-password")
def update_password(
    password_data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return change_password(db, current_user["id"], password_data)
