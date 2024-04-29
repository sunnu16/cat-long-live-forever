#회원가입 로그인 탈퇴

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi import status
from datetime import datetime
from model.models import User_tb


# user 조회

def get_user_id(user_id : int, db : Session):
    user = db.query(User_tb).filter(User_tb.id == user_id).first()

    if user :
        return {

            "status" : status.HTTP_200_OK,
            "message" : "user 조회 성공",
            "data" : user
        }
    else : 
        return{
            
            "status" : status.HTTP_404_NOT_FOUND,
            "message" : "일치하는 user가 존재하지 않습니다"
    }


#로그인

#회원가입

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