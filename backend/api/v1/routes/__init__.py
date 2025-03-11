from fastapi import APIRouter
from api.v1.routes.authentication import auth
from api.v1.routes.user_management import user

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(auth)
api_version_one.include_router(user)

