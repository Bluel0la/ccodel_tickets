import uvicorn
from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from api.db.database import create_database
from api.v1.routes import api_version_one
from dotenv import load_dotenv
import os
from datetime import datetime
from api.db.database import get_db

load_dotenv(".env")

gcs_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield
    ## write shutdown logic below yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def update_last_active(request: Request, call_next):
    response = await call_next(request)

    user = request.state.user
    if user and user.role == "support":
        db = next(get_db())
        user.last_active = datetime.utcnow()
        db.commit()

    return response


origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "https://ccodel-tickets-avab.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_version_one)
# app.include_router(users, tags=["Users"])


@app.get("/", tags=["Home"])
async def get_root(request: Request) -> dict:
    return {
        "message": "Welcome to API",
        "URL": "",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
