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
from datetime import datetime
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



#bcrypt 비번 암호화
pwd_context = CryptContext(schemes= ['bcrypt'], deprecated= "auto")


#회원가입
def create_user(new_user : schema.CreateUser, db : Session):

    new_user = UserTb(

        email = new_user.email,
        password = pwd_context.hash(new_user.password),
        #password = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
        created_at = new_user.created_at
    )

    db.add(new_user)
    db.commit()


#email 존재유무 확인
def exist_email(new_user : schema.CreateUser, db : Session):

    return db.query(UserTb).filter(

        UserTb.email == new_user.email
        ).first()





#로그인
def check_pwd(new_password, hashed_password):
    return pwd_context.verify(new_password, hashed_password)













#회원 탈퇴
