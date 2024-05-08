# 일반 회원가입 / 로그인 / 탈퇴

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from model.models import UserTb
from database import schema

from passlib.context import CryptContext
from datetime import timedelta, datetime
import bcrypt
import jwt


#########

from database.connection import get_db

    

# user 조회
def get_user_id(user_id : int, db : Session):
    user = db.query(UserTb).filter(UserTb.id == user_id).first()

    if user :
        return user
    else :
        return None



# bcrypt 비번 암호화
pwd_context = CryptContext(schemes= ['bcrypt'], deprecated= "auto")


# 회원가입
def create_user(new_user : schema.CreateUser, db : Session):

    new_user = UserTb(

        email = new_user.email,
        password = pwd_context.hash(new_user.password),
        #password = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
        username = new_user.username,
        created_at = new_user.created_at
    )

    db.add(new_user)
    db.commit()



 # email 존재유무 확인 
def exist_email(new_user : schema.CreateUser, db : Session):

    return db.query(UserTb).filter(UserTb.email == new_user.email).first()


# 로그인

 #비번 체크
def check_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 로그인 토큰 생성
def create_access_token(data : dict, expire_delta : timedelta | None = None):
    
    to_encode = data.copy()

    if expire_delta :
        expire = datetime + expire_delta
    else :
        expire = datetime +timedelta(minutes=15)
    
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, Key.SECRET_KEY, algorithm= Key.ALGORITHM)

    return encoded_jwt


'''
# username 존재유무 확인
def exist_username(login_user : schema.Login, db : Session):

    return db.query(UserTb).filter(login_user.email == UserTb.email).first()
'''













#회원 탈퇴
#비밀번호 찾기 - 임의비번 생성 후, 해당 계정 메일로 발송