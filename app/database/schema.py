# 스키마

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator # pydantic v2에선 validator 사용x
from fastapi import HTTPException
from datetime import datetime


# 회원가입
class create_user(BaseModel):
    email : EmailStr
    password : str
    created_at : datetime




'''
# 회원가입 유효성 검증

#빈칸 검증
@field_validator('email', 'password')

def check_empty(cls, v):
    if not v or v.isspace():
        raise HTTPException(
            status_code=422,
            detail = "필수 항목을 입력해주세요"
        )
    return v


#비밀번호 조건
@field_validator('password')

def check_pw(cls, v):

    if len(v) < 8:

        raise HTTPException(
            status_code=422,
            detail= "8자리 이상 입력해주세요"
        )
    if not any(char.isdigit() for char in v):

        raise HTTPException(
            status_code=422,
            detail= "비밀번호에 숫자를 포함하여 입력해주세요"
        )
    if not any(char.isalpha() for char in v):

        raise HTTPException(
            status_code=422,
            detail= "비밀번호에 영문을 포함하여 입력해주세요"
        )
    return v
'''
