 # 엔드포인트 / 라우팅

from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.connection import get_db
from crud import users 
#oAuth, home, health, diary  


#user router

user = APIRouter(
    prefix= "/user"
)


#user 조회
@user.get("/{user_id}")

def get_user(user_id : int, db : Session = Depends(get_db)):

    response = users.get_user_id(user_id = user_id, db = db)
    return response




'''
#user 생성
@user.post("/")
def create_user(request : Request, db : Session = Depends(get_db)):
    
    user_data = request.json()

    response = users.create_user(user_data = user_data, db = db)

    return response
'''






#oAuth router
#home router
#health router
#diary router

