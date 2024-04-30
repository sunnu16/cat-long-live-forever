# main app

from fastapi import FastAPI
from routers import router


def create_app() -> FastAPI:

    _app = FastAPI()
    _app.include_router(router)

    return _app

app = create_app()

#파이썬 접근제한자