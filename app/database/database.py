#datavases 연결
#중요 내용 git에 올라가지 않도록 주의

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base

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
engine = create_engine(
    DB_URL
)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
'''