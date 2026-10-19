from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.core.dependencies import get_current_user, require_admin
from api.db.database import get_db
from api.utils.user_service import (
    change_password,
    count_active_admins,
    create_user,
    get_all_users,
    get_user_by_id,
    soft_delete_user,
    update_user_details,
)
from api.v1.models.refresh_tokens import RefreshToken
from api.v1.models.user import User
from api.v1.schemas.UserRegister import AdminUserCreate, RoleEnum, UserOut
from api.v1.schemas.user_management import ChangePassword, UserUpdate

user = APIRouter(prefix="/users", tags=["Users"])


@user.get("/", response_model=List[UserOut])
def list_users(
    role: Optional[RoleEnum] = Query(None),
    is_active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_all_users(
        db,
        role=role.value if role else None,
        is_active=is_active,
        search=search,
        skip=skip,
        limit=limit,
    )


@user.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return create_user(db, user_data)


@user.put("/me/password")
def update_own_password(
    password_data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_password(db, current_user.user_id, password_data)


@user.put("/change-password", include_in_schema=False)
def update_password_legacy(
    password_data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_password(db, current_user.user_id, password_data)


@user.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin" and current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return get_user_by_id(db, user_id)


@user.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_admin = current_user.role == "admin"
    is_self = current_user.user_id == user_id

    if not is_admin and not is_self:
        raise HTTPException(status_code=403, detail="Access denied")

    updates = user_data.model_dump(exclude_unset=True)

    if not is_admin:
        forbidden_fields = {"is_active", "role"}
        if forbidden_fields.intersection(updates.keys()):
            raise HTTPException(
                status_code=403,
                detail="Only admins can change account status or role",
            )

    if is_self and not is_admin:
        updates.pop("matric_number", None)
        updates.pop("is_active", None)
        updates.pop("role", None)

    if is_self and is_admin and (
        updates.get("is_active") is False
        or ("role" in updates and updates["role"] != RoleEnum.admin)
    ):
        raise HTTPException(
            status_code=400,
            detail="Admins cannot deactivate or demote their own account",
        )

    target_user = get_user_by_id(db, user_id)
    new_role = updates.get("role")
    if (
        target_user.role == "admin"
        and new_role is not None
        and new_role != RoleEnum.admin
        and count_active_admins(db, exclude_user_id=user_id) == 0
    ):
        raise HTTPException(
            status_code=400, detail="Cannot demote the last active admin"
        )

    updated_user = update_user_details(db, user_id, user_data)

    if updates.get("is_active") is False:
        db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
        db.commit()

    return updated_user


@user.delete("/{user_id}")
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Admins cannot deactivate their own account"
        )

    target_user = get_user_by_id(db, user_id)
    if (
        target_user.role == "admin"
        and count_active_admins(db, exclude_user_id=user_id) == 0
    ):
        raise HTTPException(
            status_code=400, detail="Cannot deactivate the last active admin"
        )

    return soft_delete_user(db, user_id)
