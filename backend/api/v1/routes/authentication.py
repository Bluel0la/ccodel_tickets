from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.core.config import get_settings
from api.core.dependencies import get_current_user
from api.db.database import get_db
from api.utils.authentication import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from api.v1.models.refresh_tokens import RefreshToken
from api.v1.models.revoked_tokens import RevokedToken
from api.v1.models.user import User
from api.v1.schemas.UserRegister import UserCreate, UserSignin

auth = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None


def _token_expiry(payload: dict) -> datetime:
    expires_at = payload.get("exp")
    if not expires_at:
        return datetime.utcnow() + timedelta(days=1)
    return datetime.utcfromtimestamp(int(expires_at))


@auth.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
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

    new_user = User(
        matric_number=user_data.matric_number,
        first_name=user_data.firstname,
        last_name=user_data.lastname,
        email=email,
        password=hash_password(user_data.password),
        role="student",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.user_id}


@auth.post("/login")
def login(request: UserSignin, db: Session = Depends(get_db)):
    email = request.email.lower()
    user = db.query(User).filter(func.lower(User.email) == email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    token_data = {"sub": user.email, "user_id": str(user.user_id)}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    db.add(
        RefreshToken(
            user_id=user.user_id,
            token=refresh_token,
            expires_at=datetime.utcnow()
            + timedelta(days=get_settings().refresh_token_expire_days),
        )
    )
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": get_settings().access_token_expire_minutes * 60,
        "user": {
            "user_id": str(user.user_id),
            "matric_number": user.matric_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role,
        },
    }


@auth.get("/me")
def get_current_user_details(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "matric_number": current_user.matric_number,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


@auth.post("/refresh-token")
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    payload = decode_token(request.refresh_token, expected_type="refresh")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    stored_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == request.refresh_token)
        .first()
    )
    if not stored_token or stored_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=401, detail="Invalid or expired refresh token"
        )
    if (
        db.query(RevokedToken)
        .filter(RevokedToken.token == request.refresh_token)
        .first()
    ):
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    token_data = {"sub": user.email, "user_id": str(user.user_id)}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    db.delete(stored_token)
    db.add(
        RefreshToken(
            user_id=user.user_id,
            token=new_refresh_token,
            expires_at=datetime.utcnow()
            + timedelta(days=get_settings().refresh_token_expire_days),
        )
    )
    db.add(
        RevokedToken(
            token=request.refresh_token,
            expires_at=stored_token.expires_at,
        )
    )
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": get_settings().access_token_expire_minutes * 60,
    }


@auth.post("/logout")
def logout(
    request: Optional[LogoutRequest] = None,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_token(token, expected_type="access")
    if not db.query(RevokedToken).filter(RevokedToken.token == token).first():
        db.add(
            RevokedToken(
                token=token,
                expires_at=_token_expiry(payload),
            )
        )

    if request and request.refresh_token:
        refresh_payload = decode_token(
            request.refresh_token, expected_type="refresh"
        )
        stored_token = (
            db.query(RefreshToken)
            .filter(RefreshToken.token == request.refresh_token)
            .first()
        )
        if stored_token:
            db.delete(stored_token)
        if not db.query(RevokedToken).filter(
            RevokedToken.token == request.refresh_token
        ).first():
            db.add(
                RevokedToken(
                    token=request.refresh_token,
                    expires_at=_token_expiry(refresh_payload),
                )
            )

    db.commit()
    return {"message": "Logged out successfully"}
