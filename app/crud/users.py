# 일반 회원가입 / 로그인 / 탈퇴

from sqlalchemy.orm import Session

from app.model.models import User_tb
from app.database.schema import create_user

from passlib.context import CryptContext
import bcrypt
import jwt



#bcrypt 비번 암호화
pwd_context = CryptContext(schemes= ['bcrypt'], deprecated= "auto")


# user 조회

def get_user_id(user_id : int, db : Session):
    user = db.query(User_tb).filter(User_tb.id == user_id).first()

    if user:
        return user
    else:
        return None




#회원가입
def get_user_email(email : str, db : Session):
    return db.query(User_tb).filter(User_tb.email == email).first()


def create_user(new_user : create_user, db : Session):

    user = User_tb(
        email = new_user.email,
        password = pwd_context.hash(new_user.password),
        #password = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
        created_at = new_user.created_at

    )
    db.add(user)
    db.commit()


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