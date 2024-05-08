#db 중요 info 불러오기

import os
from dotenv import load_dotenv


load_dotenv()

class Setting:
    DB_USERNAME: str = os.getenv("DB_id")
    DB_PASSWORD = os.getenv("DB_pw")
    DB_HOST: str = os.getenv("DB_host")
    DB_PORT: str = os.getenv("DB_port")
    DB_DATABASE: str = os.getenv("DB_database")

    DB_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    #f-string


class SettingKey:
    SECRET_KEY : str = os.getenv("SECRET_KEY")
    ALGORITHM : str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

