# 스키마

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator # pydantic v2에선 validator (x) / field_validator (o)

from email_validator import EmailNotValidError
from email_validator import validate_email

from fastapi import HTTPException
from datetime import datetime



# 회원가입
class CreateUser(BaseModel):
    email : EmailStr
    password : str
    created_at : datetime


# 빈 값 핸들링
    @field_validator('email', 'password')

    # 빈 값 핸들링
    def not_empty(cls, v):
        if not v or not v.strip():

            raise HTTPException(

                status_code= 422,
                detail= "이메일, 비밀번호를 입력해주세요"
            )
        return v

#email form 핸들링
    @field_validator('email')

    def validate_email(cls, v):
        try:
            validate_email(v)
        except EmailNotValidError:
            raise ValueError("올바른 형식의 이메일을 입력해주세요")
        return v
 #에러 메세지 ("올바른 형식의 이메일을 입력해주세요") 확인요망 이유 못 찾음


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



#로그인
class Token(BaseModel):
    access_token : str
    token_type : str
    email : EmailStr



    

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
