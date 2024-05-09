from fastapi import APIRouter, Depends, Request, Response
from fastapi import status
from fastapi import HTTPException

#Fastapi oAuth2에선 username or password 양식을 사용해야함 -> 데이터 안에 user-name / email 작동x
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import jwt

from datetime import timedelta, datetime



from database.connection import get_db
from crud import users
from crud.users import create_access_token
from database import schema

from config.config import SettingKey #token




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
    exist_user = users.exist_email(new_user.email, db)

    if exist_user:
        raise HTTPException(
            
            status_code= status.HTTP_409_CONFLICT,
            detail= "이미 존재하는 계정입니다"
        )
    
    #회원가입
    users.create_user(new_user = new_user, db = db)

    return HTTPException(

        status_code= status.HTTP_200_OK,
        detail= "회원가입 성공"
        ) 



SECRET_KEY = "b2bf882e7f7f6fee20b3fbf7441e83a3087a0152ec506a255b575d9066f012ee"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#문제점 - .env -> config.config 안의 토큰 관련 위 3값을 인식 못하는 / 헤더, 쿠키



# 로그인 router / 토큰 - 헤더
@router.post("/login")

def login(login_data : schema.Login = Depends(), db : Session = Depends(get_db)):

    user = users.exist_email(login_data.email, db)

    # email check
    if not user :
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "email 혹은 비밀번호가 일치하지 않습니다",
            headers= {"WWW-Authenticate": "Bearer"}
        )
    
    response = users.check_pwd(login_data.password, user.password)

    # pwd check
    if not response :
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "email 혹은 비밀번호가 일치하지 않습니다",
            headers= {"WWW-Authenticate": "Bearer"}
        )
    
    # 토큰 - 헤더
    data = {
        "sub" : user.email,
        "exp" : datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm= ALGORITHM)

    return {
        "access_token" : access_token,
        "token_type" : "bearer",
        "email" : user.email,
        "status" : status.HTTP_200_OK,
        "detail" : "로그인 성공",

    }



'''# 로그인 router / 토큰 - 쿠키
@router.post("/login")

def login(login_data : schema.Login = Depends(), db : Session = Depends(get_db)):

    user = users.exist_email(login_data.email, db)

    # email check
    if not user :
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "email 혹은 비밀번호가 일치하지 않습니다"
        )
    
    response = users.check_pwd(login_data.password, user.password)

    # 토큰 생성
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    #access_token_expires = timedelta(minutes= SettingKey.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(data = {"sub" : user.email}, expires_delta = access_token_expires)
    #TypeError: create_access_token() got an unexpected keyword argument 'expires_delta'
    
    # 쿠키에 저장
    response.set_cookie(key="access_token", value = access_token, expires = access_token_expires, httponly=True)

    # pwd check
    if not response :
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "email 혹은 비밀번호가 일치하지 않습니다"
        )
    
    return schema.LoginToken(access_token= access_token, token_type= "bearer")
'''


# 로그아웃 / 쿠키

@router.get("/logout")

def logout(response : Response, request : Request):
    access_token = request.cookies.get("access_token")

    #쿠키 삭제
    response.delete_cookie(key= "access_token")

    return HTTPException(

        status_code= status.HTTP_200_OK,
        detail= "로그아웃 성공"
    )





# 회원탈퇴
#email 일치 확인 후, 비번 일치 확인  다음 삭제
@router.delete("/delete")
def delete(delete_data : schema.DeleteUser, db : Session = Depends(get_db)):

    #회원 존재 유무 확인 (email)
    user = users.exist_email(delete_data.email, db)
    if not user:

        raise HTTPException(            
            status_code= status.HTTP_409_CONFLICT,
            detail= "email 혹은 비밀번호가 일치하지 않습니다"
        )
    
    response = users.check_pwd(delete_data.password, user.password)

    # pwd check
    if not response :
        raise HTTPException(

            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "email 혹은 비밀번호가 일치하지 않습니다"
        )
    
    users.delete_user(delete_data = delete_data, db = db)

    return HTTPException(
        
        status_code= status.HTTP_200_OK,
        detail= "회원탈퇴 성공"
        )




#비밀번호 찾기 (재설정)
#email 일치 확인 후, 임의 비번(랜덤 조건:영문 대소문자, 숫자) 생성 -> 해당 email로 임의 비번 발송
@router.post("/find-pwd")
def find(find_data : schema.FindPwd, db : Session = Depends(get_db)):

    #회원 존재 유무 확인 (email)
    user = users.exist_email(find_data.email, db)
    if not user:

        raise HTTPException(            
            status_code= status.HTTP_409_CONFLICT,
            detail= "email이 일치하지 않습니다"
        )
    
    #email 유저 맞으면 임의변경 된 비번을 해당 계정 이메일로 발송하기
    if user :
        users.change_pwd(find_data)
    
