import os

from dotenv import load_dotenv

load_dotenv()


class DataBase:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')

    USER = f"{DB_USER}:{DB_PASS}"
    DATABASE = f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    URL_DB = f"postgresql+asyncpg://{USER}@{DATABASE}"


class Config:
    ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")


class AuthJWT:
    access_token_expire_days: int = 3


class Settings:
    db: DataBase = DataBase()
    config: Config = Config()
    auth_jwt: AuthJWT = AuthJWT()


settings: Settings = Settings()
