from fastapi import APIRouter, Depends, Request
from fastapi import status

from sqlalchemy.orm import Session
from app.database.connection import get_db

from app.crud import users


router = APIRouter()

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    response = users.get_user_id(user_id=user_id, db=db)

    if response :
        return {

            "status" : status.HTTP_200_OK,
            "detail" : "user 조회 성공",
            "data" : response
        }
    else :
        return{

            "status" : status.HTTP_404_NOT_FOUND,
            "detail" : "일치하는 user가 존재하지 않습니다"
    }
