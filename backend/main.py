from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.config import get_settings
from api.db.database import create_database
from api.v1.routes import api_version_one

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_version_one)


@app.get("/", tags=["Home"])
async def get_root():
    return {"message": "Welcome to the CCODEL Tickets API", "status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
