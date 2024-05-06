# main app - api/api 받아오기

from fastapi import FastAPI
from api.api import api_router


def create_app() -> FastAPI:

    _app = FastAPI()
    _app.include_router(api_router)

    return _app

app = create_app()

#파이썬 접근제한자