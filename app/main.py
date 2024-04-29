# main app

from fastapi import FastAPI
from router.routers import router


def create_app() -> FastAPI:

    _app = FastAPI()
    _app.include_router(router)

    return _app

app = create_app()



'''
from typing import Union
from fastapi import Depends
from fastapi import Path
'''