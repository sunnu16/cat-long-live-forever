from fastapi import APIRouter, Depends, Request, Response
from fastapi import status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import jwt

from datetime import timedelta, datetime


from database.connection import get_db
from crud import users
from database import schema

from config.config import SettingKey





router = APIRouter()


# user 조회 router
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    response = users.get_user_id(user_id=user_id, db=db)

    if response :
        return{

            "status" : status.HTTP_200_OK,
            "detail" : "회원 조회 성공",
            "data" : response
        }
    else :
        return {

            "status" : status.HTTP_404_NOT_FOUND,
            "detail" : "일치하는 user가 존재하지 않습니다"
    }




#회원가입 router
@router.post("/signup")

def signup(new_user : schema.CreateUser, db : Session = Depends(get_db)):

    #회원 존재 유무 확인 (email)
    exist_user = users.exist_email(new_user = new_user, db = db)

    if exist_user:
        raise HTTPException(
            status_code= 409,
            detail= "이미 존재하는 계정입니다"
        )
    
    signup_user = users.create_user(new_user = new_user, db = db)

    if signup_user:
        raise HTTPException(
            status_code= 200,
            detail= "회원가입 성공"
        ) 
    #기능 문제없음 단, response body에 detail= "회원가입 성공" 안뜸 - null




# 로그인  -->
 # 문제점 : Fastapi oAuth2에선 username or password 양실을 사용해야함 -> user-name / email 작동x
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





'''
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








# 로그아웃
# 회원탈퇴