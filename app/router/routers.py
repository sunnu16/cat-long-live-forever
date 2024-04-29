 # 엔드포인트 / 라우팅

from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi import HTTPException

from crud import users
from database import schema

#user router
router = APIRouter()

@router.get("/user/{user_id}")

def get_user(user_id : int, db : Session = Depends(get_db)):

    response = users.get_user_id(user_id = user_id, db = db)
    
    return response



#회원가입 router


@router.post("/signup")
def signup(new_user : schema.create_user, db : Session = Depends(get_db)):

    # 존재 여부
    user = users.get_user_email(new_user.email, db)

    if user:
        raise HTTPException(
            status_code= 409,
            detail= "user가 이미 존재합니다"
        )

    # 회원가입
    users.create_user(new_user, db)

    return HTTPException(
        status_code= 200,
        detail= "회원가입 성공"
    )




'''
#로그인 router
login = APIRouter(
    prefix = "/login"
)



#회원탈퇴 router
remove = APIRouter(
    prefix = "/remove"
)





#user 회원가입
@signup.post("/")
def create_user(request : Request, db : Session = Depends(get_db)):
    
    user_data = request.json()

    response = users.create_user(user_data = user_data, db = db)

    return response
'''






#oAuth router
#home router
#health router
#diary router

