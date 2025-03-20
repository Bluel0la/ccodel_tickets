import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from api.db.database import create_database, get_db
from api.v1.routes import api_version_one
from api.utils.authentication import get_current_user  # Import your auth function
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv(".env")

gcs_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield  # Add shutdown logic if needed


app = FastAPI(lifespan=lifespan)


## ✅  Add Authentication Middleware Here
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None  # Default to None
        try:
            db: Session = next(get_db())
            user = await get_current_user(request, db)
            request.state.user = user  # Assign user
        except Exception:
            pass  # Ignore errors (user will be None)

        response = await call_next(request)
        return response


app.add_middleware(AuthMiddleware)  # ✅ Apply Middleware Here


## ✅  Fix `update_last_active`
@app.middleware("http")
async def update_last_active(request: Request, call_next):
    response = await call_next(request)

    user = getattr(request.state, "user", None)  # ✅ Use `getattr` to avoid errors
    if user and getattr(user, "role", None) == "support":  # ✅ Safely check attributes
        db = next(get_db())
        user.last_active = datetime.utcnow()
        db.commit()

    return response


## ✅  CORS Middleware
origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "https://ccodel-tickets-avab.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


## ✅  Include API Routes
app.include_router(api_version_one)


@app.get("/", tags=["Home"])
async def get_root(request: Request):
    return {
        "message": "Welcome to API",
        "URL": "",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
