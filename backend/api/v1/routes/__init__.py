from fastapi import APIRouter

from api.v1.routes.analytics import analytics
from api.v1.routes.authentication import auth
from api.v1.routes.tags import tags
from api.v1.routes.tickets import tickets
from api.v1.routes.user_management import user

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(auth)
api_version_one.include_router(user)
api_version_one.include_router(tickets)
api_version_one.include_router(tags)
api_version_one.include_router(analytics)
