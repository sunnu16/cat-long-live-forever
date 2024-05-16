import os
from dotenv import load_dotenv

#db 중요 info 불러오기

load_dotenv()

class SettingKey:
    '''
    SettingKey class
    '''
    DB_USERNAME: str = os.getenv("DB_id")
    DB_PASSWORD: str = os.getenv("DB_pw")
    DB_HOST: str = os.getenv("DB_host")
    DB_PORT: str = os.getenv("DB_port")
    DB_DATABASE: str = os.getenv("DB_database")

    DB_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    #f-string

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

settingkeys = SettingKey()

'''
print(f"SettingKey: {settingkeys}")
# print(f"db: {settings.DB_USERNAME}")
print(f"secret key: {settingkeys.SECRET_KEY}")
print(f"algorithm: {settingkeys.ALGORITHM}")
print(f"expire: {settingkeys.ACCESS_TOKEN_EXPIRE_MINUTES}")
'''