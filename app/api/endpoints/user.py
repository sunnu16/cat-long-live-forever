from fastapi import APIRouter, Depends, Request, Response
from fastapi import status
from fastapi import HTTPException

#Fastapi oAuth2에선 username or password 양식을 사용해야함 -> 데이터 안에 user-name / email 작동x
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import jwt

from datetime import timedelta, datetime

from database.connection import connect_db
from crud import users
from crud.users import create_access_token_cookie
from database import schema

from database.schema import CreateUser

# from config.config import SettingKey #token
from config.config import SettingKey


from fastapi.requests import Request

router = APIRouter()


'''
contriller : 
 - model과 view 사이에서 데이터 흐름을 제어 (C는 M과 V에 대해 알고 있고, 변경 내용을 모니터링 해야함) 
 - model과 view의 역할 분리가 중요

역할 분리가 명확하지 않아보입니다. 
router에서 정의한 schema를 사용하고, 
data return하는게 과연 적절할까요?
'''



# user 조회 router
@router.get("/{user_id}")

def get_user(user_id : int, db : Session = Depends(connect_db)):
    return users.get_user_id(user_id= user_id, db= db)



#회원가입 router
@router.post("/signup")

def signup(new_user : schema.CreateUser, db : Session = Depends(connect_db)):

    #회원 존재 유무 확인 (email)
    users.exist_email(new_user.email, db)
    #회원가입
    return users.create_user(new_user = new_user, db = db)



# 로그인 router / 토큰 - 헤더
@router.post("/login")

def login(login_data : schema.Login, db : Session = Depends(connect_db)):
   
    # id_email check
    user = users.check_email(login_data.email, db)

    if user:
    # pwd check
        users.check_pwd_header(login_data.password, user.password)
    #token create
    return users.token_header(user)

    



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

    # pwd check
    if not response :
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "email 혹은 비밀번호가 일치하지 않습니다"
        )

    # 토큰 생성
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    #access_token_expires = timedelta(minutes= SettingKey.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token_cookie(data = {"sub" : user.email}, expires_delta = access_token_expires)
    #TypeError: create_access_token_cookie() got an unexpected keyword argument 'expires_delta'
    
    # 쿠키에 저장
    response.set_cookie(key="access_token", value = access_token, expires = access_token_expires, httponly=True)

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
def delete(delete_data : schema.DeleteUser, db : Session = Depends(connect_db)):

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



'''
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
    
'''