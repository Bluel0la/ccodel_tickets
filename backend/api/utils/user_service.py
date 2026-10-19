from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from api.utils.authentication import hash_password, verify_password
from api.v1.models.refresh_tokens import RefreshToken
from api.v1.models.user import User
from api.v1.schemas.UserRegister import AdminUserCreate
from api.v1.schemas.user_management import ChangePassword, UserUpdate


def get_all_users(
    db: Session,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if search:
        term = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                func.lower(User.first_name).like(term),
                func.lower(User.last_name).like(term),
                func.lower(User.email).like(term),
                func.lower(User.matric_number).like(term),
            )
        )

    return query.order_by(User.first_name.asc(), User.last_name.asc()).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: UUID):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, user_data: AdminUserCreate):
    email = user_data.email.lower()
    existing_user = (
        db.query(User)
        .filter(
            (func.lower(User.email) == email)
            | (User.matric_number == user_data.matric_number)
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email or Matric No. already registered"
        )

    user = User(
        matric_number=user_data.matric_number,
        first_name=user_data.firstname,
        last_name=user_data.lastname,
        email=email,
        password=hash_password(user_data.password),
        role=user_data.role.value,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_details(db: Session, user_id: UUID, user_data: UserUpdate):
    user = get_user_by_id(db, user_id)
    updates = user_data.model_dump(exclude_unset=True)

    if "email" in updates and updates["email"]:
        email = str(updates["email"]).lower()
        duplicate = (
            db.query(User)
            .filter(func.lower(User.email) == email, User.user_id != user_id)
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=400, detail="Email already in use")
        updates["email"] = email

    if "matric_number" in updates and updates["matric_number"]:
        duplicate = (
            db.query(User)
            .filter(
                User.matric_number == updates["matric_number"],
                User.user_id != user_id,
            )
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=400, detail="Matric number already in use"
            )

    if "role" in updates and updates["role"] is not None:
        updates["role"] = updates["role"].value

    for key, value in updates.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(db: Session, user_id: UUID):
    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()
    return {"message": "User deactivated"}


def change_password(db: Session, user_id: UUID, password_data: ChangePassword):
    user = get_user_by_id(db, user_id)

    if not verify_password(password_data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user.password = hash_password(password_data.new_password)
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()
    return {"message": "Password updated successfully"}


def count_active_admins(db: Session, exclude_user_id: Optional[UUID] = None) -> int:
    query = db.query(User).filter(User.role == "admin", User.is_active.is_(True))
    if exclude_user_id:
        query = query.filter(User.user_id != exclude_user_id)
    return query.count()
