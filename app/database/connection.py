#datavases 연결

'''
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.config import setting
'''

from database.session import SessionLocal

def get_db():
    db = SessionLocal()

    try:
        yield db  # DB 연결 -> session 시작

    finally:
        db.close()






















'''
#DB_URL = 'mysql+pymysql://{userid}:{pw}@{db_host}/{db_name}'


class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn




'''