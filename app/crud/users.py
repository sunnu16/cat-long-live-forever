# 일반 회원가입 / 로그인 / 탈퇴

from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi import status


from model.models import UserTb
from database import schema


from passlib.context import CryptContext
from datetime import datetime
import bcrypt
import jwt


#########

from database.connection import get_db

from database import schema
from fastapi import Depends

'''
# user 조회
def get_user_id(user_id : int, db : Session):

    user = db.query(UserTb).filter(UserTb.id == user_id).first()

    return user
'''


# email 조회
def get_user_email(new_user : schema.CreateUser, db : Session):
    user = db.query(UserTb).filter(UserTb.email == new_user.email).first()
    return user


    

# user 조회
def get_user_id(user_id : int, db : Session):
    user = db.query(UserTb).filter(UserTb.id == user_id).first()

    if user :
        return {

            "status" : status.HTTP_200_OK,
            "detail" : "user 조회 성공",
            "data" : user
        }
    else : 
        return{
            
            "status" : status.HTTP_404_NOT_FOUND,
            "detail" : "일치하는 user가 존재하지 않습니다"
    }




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
    
    if new_user.email :
        raise HTTPException(
            status_code= 400,
            detail= "이미 존재하는 email입니다"
        )
    else :
        raise HTTPException(
            status_code= 200,
            detail= "회원가입 성공"
        )





#로그인
def check_pwd(new_password, hashed_password):
    return pwd_context.verify(new_password, hashed_password)




#로그인











#회원 탈퇴




'''
def get_user_id(user_id : int, db : Session):
    user = db.query(User_tb).filter(User_tb.id == user_id).first()

    if user is not non:
        return {

            "status" : status.HTTP_200_OK,
            "detail" : "user 조회 성공",
            "data" : user
        }
    else : 
        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,
            detail='일치하는 user가 존재하지 않습니다'
            )
'''