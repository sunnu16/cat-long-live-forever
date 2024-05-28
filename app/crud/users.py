# 일반 회원가입 / 로그인 / 탈퇴

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Depends

from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt

from model.models import UserTb
from database import schema

from config.config import SettingKey


import random, string


'''
view : 
 - C에서 받은 M의 데이터를 시각적으로 보여주기 위한 역할
 - 레이아웃과 화면 처리 (model, controiller의 정보를 따로 저장 x
 - M C의 변경 발생 시, 변경에 대한 처리방법을 구현해야만함
'''



# user id 조회 로직
class GetUserId:
    def get_user_id(user_id : int, db : Session):

        user = db.query(UserTb).filter(UserTb.id == user_id).first()   
        db.close

        if user :
            return{

                "status" : status.HTTP_200_OK,
                "detail" : "회원 조회 성공",
                "data" : user
            }
            
        if not user :
            return{

                "status" : status.HTTP_404_NOT_FOUND,
                "detail" : "일치하는 회원이 존재하지 않습니다"
            }



# bcrypt 비번 암호화
pwd_context = CryptContext(schemes= ['bcrypt'], deprecated= "auto")  



# 회원가입 로직
class SignUp:

    # 회원가입 - email 존재유무 확인 
    def exist_email(email : str, db : Session):

        res = db.query(UserTb).filter(UserTb.email == email).first()
        db.close
        
        if res :
            raise HTTPException(

                status_code= status.HTTP_409_CONFLICT,
                detail= "이미 존재하는 계정입니다"
            )
        return res


    # 유저 생성
    def create_user(new_user : schema.CreateUser, db : Session):

        new_user = UserTb(

            email = new_user.email,
            password = pwd_context.hash(new_user.password),
            #password = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
            created_at = new_user.created_at
        )

        db.add(new_user)
        db.commit()

        return HTTPException(

            status_code= status.HTTP_200_OK,
            detail= "회원가입 성공"
        )



# 로그인 로직
class Login:

    # 로그인 - email 존재x
    def check_email(email : str, db : Session):

        res = db.query(UserTb).filter(UserTb.email == email).first()
        db.close

        if not res :
            raise HTTPException(

                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "email 혹은 비밀번호가 일치하지 않습니다",
                headers= {"WWW-Authenticate": "Bearer"}

            )
        return res
        
    
    #로그인 - pwd 체크
    def check_pwd(plain_password : str, hashed_password : str):

        pwd = pwd_context.verify(plain_password, hashed_password)

        if not pwd :
            
            raise HTTPException(

                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "email 혹은 비밀번호가 일치하지 않습니다",
                headers= {"WWW-Authenticate": "Bearer"}
            )
        return pwd
        

    # 토큰 생성 - header
    def token_header(user : str):
        # 토큰 - 헤더
        data = {

            "sub" : user.email,
            "exp" : datetime.utcnow() + timedelta(minutes= SettingKey.ACCESS_TOKEN_EXPIRE_MINUTES),
        } # timedelta(minutes= float(SettingKey.ACCESS_TOKEN_EXPIRE_MINUTES))

        access_token = jwt.encode(data, SettingKey.SECRET_KEY, algorithm= SettingKey.ALGORITHM)

        return {

            "access_token" : access_token,
            "token_type" : "bearer",
            "email" : user.email,
            "status" : status.HTTP_200_OK,
            "detail" : "로그인 성공",
        }

   

# 회원탈퇴 로직
class Delete:

    # 회원삭제
    def delete_user(delete_data : schema.DeleteUser, db : Session):
    
        db.query(UserTb).filter(UserTb.email == delete_data.email).delete()
        db.commit()
        
        return HTTPException(      

            status_code= status.HTTP_200_OK,
            detail= "회원탈퇴 성공"
            )


'''    # 회원탈퇴 - email 검증
    def check_email(email : str, db : Session):

        res = db.query(UserTb).filter(UserTb.email == email).first()
        db.close

        if not res :
            raise HTTPException(

                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "email 혹은 비밀번호가 일치하지 않습니다",
                headers= {"WWW-Authenticate": "Bearer"}

            )
        return res
    

    #회원탈퇴 - pwd 체크
    def check_pwd_header(plain_password : str, hashed_password : str):

        pwd = pwd_context.verify(plain_password, hashed_password)

        if not pwd :
            
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "email 혹은 비밀번호가 일치하지 않습니다",
                headers= {"WWW-Authenticate": "Bearer"}
            )
        return pwd'''
    






''' #pwd 체크
def check_pwd(plain_password : str, hashed_password :str):
    return pwd_context.verify(plain_password, hashed_password)'''
    








# 로그인 토큰 생성 -쿠키
def create_access_token_cookie(data : dict, expire_delta : timedelta | None = None):
    
    to_encode = data.copy()

    if expire_delta :
        expire = datetime + expire_delta
    else :
        expire = datetime +timedelta(minutes=15)
    
    to_encode.update({"exp" : expire})
    
    encoded_jwt = jwt.encode(to_encode, SettingKey.SECRET_KEY, algorithm= SettingKey.ALGORITHM)

    return encoded_jwt



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





'''
# 비밀번호 재설정 / change_pwd(임의 비번 생성 + 변경 저장)
def change_pwd(change_data : schema.FindPwd, db : Session):

    

    new_random_pwd = pwd_context.hash(schema.FindPwd.password)

    db.add(change_data)
    db.commit()'''



#비밀번호 찾기 - 임의비번 생성 후, 해당 계정 메일로 발송