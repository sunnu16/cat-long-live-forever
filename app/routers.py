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

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig



router = APIRouter()


#user 조회 router
@router.get("/user/{user_id}")





#회원가입 router
@router.post("/signup")

def signup(new_user : schema.CreateUser, db : Session = Depends(get_db)):
    users.create_user(db= db, new_user= new_user)







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


#oAuth router
#home router
#health router
#diary router


'''
@router.post("/login")

def login(response : Response, login_user: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):

    #회원 존재 유무 확인 (email)
    user = users.exist_email(login_user.username, db)

    # 계정 존재x
    if not user:
        raise HTTPException(
            status_code= 400,
            detail= "계정이 존재하지 않습니다"
        )
    
    # 로그인
    response = users.check_pwd(login_user.password, user.password)

    # token 생성
    access_token_expires = timedelta(minutes= SettingKey.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = users.create_access_token(data={"sub" : user.username}, expires_delta = access_token_expires)

    #쿠키에 
    response.set_cookie(key="access_token", value= "access_token", expires= access_token_expires, httponly= True)

    if not response:
        raise HTTPException(

            status_code= 400,
            detail= "email 혹은 비밀번호가 일치하지 않습니다"
        )
    return {

        "status" : status.HTTP_200_OK,
        "detail" : "로그인 성공",
        "data" : schema.Token(access_token = access_token, token_type= "bearer")
        }






@router.post("/login")

def login(login_user: schema.Login = Depends(), db : Session = Depends(get_db)):

    #회원 존재 유무 확인 (email)
    exist_user = users.exist_email_1(login_user = login_user, db = db)

    # 계정 존재x
    if not exist_user:
        raise HTTPException(
            status_code= 400,
            detail= "email 또는 비밀번호을 잘못 입력했습니다"
        )
    
    # 로그인
    response = users.check_pwd(login_user.password, exist_user.password)

    # token 생성
    access_token_expires = timedelta(minutes= Key.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub" : exist_user.email}, expires_delta = access_token_expires)

    if not response:
        raise HTTPException(
            status_code= 400,
            detail= "email 혹은 비밀번호가 일치하지 않습니다"
        )
    return {
        "status" : status.HTTP_200_OK,
        "detail" : "로그인 성공",
        "data" : schema.Token(access_token = access_token, token_type= "bearer")
        }




'''
