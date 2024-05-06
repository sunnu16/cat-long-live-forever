# 스키마

from pydantic import BaseModel
from pydantic import EmailStr # 사용시 지정 error message 사용불가
from pydantic import field_validator # pydantic v2에선 validator (x) / field_validator (o)

from email_validator import EmailNotValidError
from email_validator import validate_email

from fastapi import HTTPException
from datetime import datetime

from model.models import UserTb




# User
class CreateUser(BaseModel):
    email : str
    password : str
    created_at : datetime




# 회원가입

# 빈 값 핸들링
    @field_validator('email', 'password')

    def not_empty(cls, v):
        if not v or not v.strip():

            raise HTTPException(

                status_code= 422,
                detail= "이메일, 비밀번호를 입력해주세요"
            )
        return v 


#비밀번호 handling
    @field_validator('password')    
    def pwd_check(cls, v):

        # 10자리 이상 입력
        if len(v) < 10:
            raise HTTPException(

                status_code= 422,
                detail= "비밀 번호를 10자리 이상 입력하세요"
            )
        
        # 숫자 포함
        if not any(char.isdigit() for char in v):            
            raise HTTPException(

                status_code=422,
                detail= "비밀번호에 숫자를 포함하여 입력해주세요"             
            )
        # 문자 포함
        if not any(char.isalpha() for char in v):
            raise HTTPException(

                status_code=422,
                detail= "비밀번호에 영문을 포함하여 입력해주세요"
                )
        return v


#email form 핸들링
    @field_validator('email')

    def validate_email(cls, v):
        try:
            validate_email(v)
        except EmailNotValidError:
            raise HTTPException(
                status_code=422,
                detail= "올바른 형식의 이메일을 입력해주세요"
                )
        return v






#로그인
class Token(BaseModel):
    access_token : str
    token_type : str
    email : EmailStr



    

