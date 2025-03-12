from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from api.db.database import get_db  
from api.v1.models.user import User 
from api.v1.schemas.UserRegister import UserCreate, UserSignin
from api.utils.authentication import hash_password, verify_password, create_access_token, decode_access_token
from api.utils.cleanup import cleanup_expired_tokens
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from api.v1.models.revoked_tokens import RevokedToken
from api.v1.models.refresh_tokens import RefreshToken
from jose import jwt, JWTError
from datetime import timedelta, timezone, datetime

load_dotenv(".env")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

auth = APIRouter(prefix="/auth", tags=["Authentication"])

@auth.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email or username already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    # Hash password
    hashed_pwd = hash_password(user_data.password)

    # Create new user
    new_user = User(
        username=user_data.username,
        first_name=user_data.firstname,
        last_name=user_data.lastname,
        email=user_data.email,
        password=hashed_pwd,
        role="user",  # Default role
        school_role=user_data.school_role  # Allow user to specify this
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.user_id}

@auth.post("/login")
def login(request: UserSignin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(days=7))  # Refresh token for 7 days

    db_refresh_token = RefreshToken(user_id=user.user_id, token=refresh_token)
    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "role": user.role,
            "school_role": user.school_role
        }
    }

@auth.get("/me")
def get_current_user_details(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
        "school_role": user.school_role,
    }


@auth.post("/logout")
def logout(
    background_tasks: BackgroundTasks,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    decoded_token = decode_access_token(token)
    
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if token is already revoked
    existing_revoked = db.query(RevokedToken).filter(RevokedToken.token == token).first()
    if existing_revoked:
        raise HTTPException(status_code=400, detail="Token already revoked")

    # Store the token in the RevokedToken table
    revoked_token = RevokedToken(
    token=token, 
    expires_at=datetime.fromtimestamp(decoded_token.get("exp"), tz=timezone.utc))
    db.add(revoked_token)
    db.commit()

    # Run cleanup in the background
    background_tasks.add_task(cleanup_expired_tokens, db)

    return {"message": "Logged out successfully"}

@auth.post("/refresh-token")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Check if refresh token exists and is valid
        stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if not stored_token:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        # Generate a new access token
        new_access_token, _ = create_access_token(data={"sub": email})

        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
