#회원가입 로그인 탈퇴

from SQLAlchemy.orm import Session
from SQLAlchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi import status
from model.models import User


# user 조회

def get_user_id(user_id : int, db : Session):
    user = db.query(User).filter(User.id == user_id).first()

    if user is not None :
        return {

            "status" : status.HTTP_200_OK,
            "detail" : "user 조회 성공",
            "data" : user
        }
    else : 
        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,
            detail= "일치하는 user 존재하지 않습니다"
            )