from fastapi import APIRouter, Depends, Request
from fastapi import status
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.connection import get_db
from crud import users
from database import schema



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

    exist_user = users.exist_email(new_user = new_user, db = db)

    if exist_user:
        raise HTTPException(
            status_code= 409,
            detail= "이미 존재하는 계정입니다"
        )
    
    signup_user = users.create_user(new_user = new_user, db = db)

    if signup_user:
        raise HTTPException(
            status_code= 200,
            detail= "회원가입 성공"
        ) 
    #기능 문제없음 단, response body에 detail= "회원가입 성공" 안뜸 - null