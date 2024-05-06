# router - api/endpoints 받아오기

from fastapi import APIRouter

from api.endpoints.user import router

api_router = APIRouter()

api_router.include_router(
    router,
    prefix="/user",
    tags=["user"],
)
