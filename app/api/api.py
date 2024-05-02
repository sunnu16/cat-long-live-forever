from fastapi import APIRouter

from app.api.endpoints.user import get_user

api_router = APIRouter()
api_router.include_router(
    get_user.router,
    prefix="/user",
    tags=["user"],
)
