# FastAPI를 실행 routes폴더들의 다른 라우트들을 불러와 포함시키는 역할

from fastapi import FastAPI
from typing import Union
from fastapi import Depends
from fastapi import Path
from fastapi import HTTPException
from pydantic import BaseModel
from app.database.database import engineconn
from app.models.models import User


'''
from app.database.database import engineconn
from pydantic import testmodel
from app.models.models import User
'''

app = FastAPI()

engine = engineconn()
session = engine.sessionmaker()

class user(BaseModel):
    email : str
    password : str

@app.get("/")
def first_get():
    example = session.query(User).all()
    return example






'''
#FastAPI
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
'''