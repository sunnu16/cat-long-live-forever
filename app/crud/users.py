# 일반 회원가입 / 로그인 / 탈퇴

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Depends

from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt, bcrypt

from model.models import UserTb
from database import schema
from config.config import SettingKey
from database.connection import get_db

import random, string




# user id 조회
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
        created_at = new_user.created_at
    )

    db.add(new_user)
    db.commit()



 # email 존재유무 확인 
def exist_email(email : str, db : Session):

    return db.query(UserTb).filter(UserTb.email == email).first()



 #pwd 체크
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
    encoded_jwt = jwt.encode(to_encode, SettingKey.SECRET_KEY, algorithm= SettingKey.ALGORITHM)

    return encoded_jwt




# 회원탈퇴
def delete_user(delete_data : schema.DeleteUser, db : Session):
   
    db.query(UserTb).filter(UserTb.email == delete_data.email).delete()
    db.commit()




# 랜덤 pwd 생성
def random_pwd():

    pwd_data = string.ascii_letters + string.digits + string.punctuation
    
    new_pwd = ''.join(random.choice(pwd_data) for _ in range(7)) # 대소문자 7자리
    new_pwd += ''.join(random.choice(string.digits) for _ in range(5)) #숫자 5자리
    new_pwd += ''.join(random.choice(string.punctuation) for _ in range(5)) #특수문자 5자리
    #mix
    mix_pw_data = ''.join(random.sample(new_pwd, len(new_pwd)))

    return mix_pw_data

# 랜덤 비밀번호 생성
new_random_pwd = random_pwd()
print(new_random_pwd)






# 비밀번호 재설정 / change_pwd(임의 비번 생성 + 변경 저장)
def change_pwd(change_data : schema.FindPwd, db : Session):

    

    random_pwd(change_data) = pwd_context.hash(schema.FindPwd.password)

    db.add(change_data)
    db.commit()










#비밀번호 찾기 - 임의비번 생성 후, 해당 계정 메일로 발송