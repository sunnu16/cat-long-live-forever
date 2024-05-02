 # 엔드포인트 / 라우팅

from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException

#fastapi에서 제공하는 OAuth2을 이용한 로그인
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from database.connection import get_db

from crud import users
from database import schema

from starlette import status



router = APIRouter()


#user 조회 router
@router.get("/user/{user_id}")

def get_user(user_id : int, db : Session = Depends(get_db)):

    response = users.get_user_id(user_id = user_id, db = db)
    
    return response



#회원가입 router  -> 수정 중
@router.post("/signup")

def signup(new_user : schema.CreateUser, db : Session = Depends(get_db)):
    users.create_user(db= db, new_user= new_user)


#, status_code= status.HTTP_204_NO_CONTENT
    









'''
#회원가입 router   -> 원래 부분
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


#로그인 routerdsfa
@router.post("/login")
def login(login_user : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):

    #회원 존재 여부
    user = users.get_user_email(login_user.email, db)

    if not user:
        raise HTTPException(
            status_code= 400,
            detail= "아이디 또는 비밀번호를 잘못 입력했습니다"
        )
    
    #로그인
    response = users.check_pwd(login_user.password, user.password)

    if not response:
        raise HTTPException(
            status_code= 400,
            detail= "아이디 또는 비밀번호를 잘못 입력했습니다"
        )
    
    return HTTPException(
        status_code= 200,
        detail= "로그인 성공"
    )




'''
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
