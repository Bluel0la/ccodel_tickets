from sqlalchemy.orm import Session
from api.v1.models.user import User
from uuid import UUID
from fastapi import HTTPException
from passlib.context import CryptContext
from api.v1.schemas.user_management import UserUpdate, ChangePassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: UUID):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user_details(db: Session, user_id: UUID, user_data: UserUpdate):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def soft_delete_user(db: Session, user_id: UUID):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False  # Assuming we have an `is_active` column
    db.commit()
    return {"message": "User deactivated"}



def change_password(db: Session, user_id: UUID, password_data: ChangePassword):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password_data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user.password_hash = pwd_context.hash(password_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
