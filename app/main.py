
from fastapi import FastAPI
from typing import Union
from fastapi import Depends
from fastapi import Path
from fastapi import HTTPException
from router.routers import user


'''
from pydantic import BaseModel
from app.database.database import engineconn
from app.models.models import User
'''


def create_app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(user)

    return _app


app = create_app()