# model 정의 

from SQLAlchemy import Column, ForeignKey, Integer, String, DateTime
from SQLAlchemy.ext.declarative import declarative_base

'''
from sqlalchemy.orm import relationship
from database.database import Base
'''

Base = declarative_base()

#users 테이블
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(250), nullable=False, index=True)
    password = Column(String(250), nullable=False)
    create_at = Column(DateTime, default=DateTime)

    #oauth_id = Column(Integer, ForeignKey(oauth.id))
    #cat_id = Column(Integer, ForeignKey(cat.id))

'''
class Oauth(Base):
    __tablename__ = "oauth"

    id = Column(Integer, primary_key=True, index=True)


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    cat_name = Column(String(50), nullable=False, index=True)
    cat_birthday = Column(DateTime, default=DateTime)
    cat_gender = Column(String(50), nullable=False, index=True)
    cat_kind = Column(String(50), nullable=False, index=True)
    cat_weight = Column(Integer, nullable=False, index=True)
    cat_pic_url = Column(String(200), nullable=False, index=True)

class Health(Base):
    __tablename__ = "health"

    id = Column(Integer, primary_key=True, index=True)
    clinic_title = Column(String(100), nullable=False, index=True)
    clinic_name = Column(String(200), nullable=False, index=True)
    clinic_at = Column(DateTime, default=DateTime)
    hospital = Column(String(100), nullable=False, index=True)
    clinic_content= Column(String(250), nullable=False, index=True)
    clinic_note = Column(String(100), nullable=False, index=True)
    edit_at = Column(DateTime, default=DateTime)
    
    #cat_id = Column(Integer, ForeignKey(cat.id))

class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True, index=True)



    #user_id = Column(Integer, ForeignKey(user.id))
    #cat_id = Column(Integer, ForeignKey(cat.id))

'''
